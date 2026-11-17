# tos-app-wallloop

将原创应用 [WallLoop](https://github.com/ericbyz/wallloop)(NAS 动态壁纸服务,Apache-2.0)
打包为 [铁威马 TOS](https://www.terra-master.com) 应用中心 **deb 类应用**(x86_64 + aarch64 双架构)。

**这是什么**:TOS deb 元数据壳 + 可复现构建脚本。WallLoop 为原创项目(冲原创档 200 元),
本仓库只做 TOS 平台封装:按《TOS 7 应用开发指南》第 8 章规范,锁定源仓 Release 的
静态二进制(CGO_ENABLED=0,Go 交叉编译)打包。

| 项目 | 值 |
|---|---|
| 应用 ID | `wallloop` |
| 应用形态 | deb 类 · 悬浮窗(`type=iframe`, `exec=false`)· 双监听面 |
| 悬浮路由 | `http://<NAS>:8181/wallloop/`(TOS nginx → 127.0.0.1:18241 管理面,前缀剥离) |
| 公开播放面 | `http://<NAS>:18240/play`(0.0.0.0,电视/平板/手机直连,只读) |
| 管理面 | `127.0.0.1:18241`(面板 + 写 API,仅 TOS 桌面悬浮窗可达,天然免鉴权) |
| 版本 | v0.1.0(见 [UPSTREAM](UPSTREAM) 锁定) |
| 许可证 | Apache-2.0(源仓与封装仓同许可) |
| 数据目录 | `/var/lib/wallloop`(壁纸库 / 缩略图 / state.json) |
| 外部依赖 | 仅 TOS 出厂 `/usr/bin/ffmpeg`(探测/缩略图/演示壁纸合成);**不打包任何媒体素材** |

## 双监听面(安全设计,承接 AdWall「面板免鉴权」叙事并扩展)

1. **管理面** `127.0.0.1:18241`:面板 + 全部管理 API(上传/删除/设置/生成)——
   只能经 TOS nginx `/wallloop/`(TOS 登录态之后)反代访问;
2. **公开面** `0.0.0.0:18240`:只读子集(播放器页 / 媒体 Range 直出 / `now`、`playlist` API)——
   电视/平板/手机浏览器直连,即动态壁纸大屏本体;管理路由在公开面一律 404。

## 悬浮窗三要素(承接 dbx/AdWall 实战结论)

1. `config.ini`:`"exec": false, "type": "iframe", "path": "/wallloop/"`;
2. `nginx/wallloop.conf`:`location /wallloop/ { proxy_pass http://127.0.0.1:18241/; }`
   (**尾斜杠剥离前缀**——面板全相对路径);`client_max_body_size 4g` 匹配上传上限;
3. 服务:systemd 单元加固(**无 MemoryDenyWriteExecute**——TOS 6.12 内核打崩 Go runtime,
   go2rtc/owncast 教训),`Restart=` 留空由平台管理生命周期。

## 目录结构

```
tos-app-wallloop/
├── config.ini            # TOS 平台元数据(规范第 8 章)
├── wallloop.lang         # 26 种语言(生成:scripts/make_lang.py)
├── wallloop.env          # 服务环境变量(双监听/端口/数据目录/ffmpeg 路径)
├── UPSTREAM              # 版本锁定(源仓 Release 资产 + SHA256)
├── DEBIAN/               # control + postinst/prerm/postrm
├── init.d/wallloop.service # systemd 单元(加固,无 MDWE)
├── nginx/wallloop.conf   # ⭐ 悬浮路由:/wallloop/ → 127.0.0.1:18241/(剥前缀,4g 上传)
├── images/icons/wallloop.svg # 原创图标(与面板 logo 同源)
├── scripts/
│   ├── fetch_upstream.sh # 下载并校验源仓资产(SHA256 强制;支持 UPSTREAM_DIST_DIR 本地构建)
│   ├── build_deb.py      # 纯 Python 的 dpkg-deb 兼容打包器(control.tar 根部 ./control)
│   ├── validate.py       # TOS 审核规则校验(含双端口一致性)
│   ├── make_lang.py      # 生成 wallloop.lang(26 locales)
│   └── bump_upstream.sh  # 升级版本(UPSTREAM/config.ini/control 联动)
├── build.sh              # 一键构建 ./build.sh [x86_64|aarch64]
└── .github/workflows/    # CI:双架构构建 + Release 发布
```

## 本地构建

依赖:bash、curl、tar、python3(任意平台;有 dpkg-deb 时自动优先)。

```bash
# 前置:源仓交叉编译产出(或等 v0.1.0 Release)
#   cd ../wallloop && ./dist.sh
export UPSTREAM_DIST_DIR=Z:/business/company/twm/wallloop/dist   # 本地 dist(免发布直接打)
./build.sh                # 双架构
./scripts/validate.py     # 元数据校验
```

产物:`build/output/wallloop_<platform>.deb` + `.sha256`。

## VM 实测 checklist(TOS 7,169.254.104.128)

- [ ] `/usr/bin/dpkg.real -i wallloop_x86_64.deb` 安装成功(postinst 建 wallloop 用户 + enable 服务)
- [ ] `systemctl status wallloop` → active;`ss -tlnp | grep -E "18240|18241"` 两监听都在
- [ ] 接线四件套(raw 安装时手动补;应用中心安装时平台自动做 init.d 拷贝):
      `systemctl enable --now wallloop` +
      `mkdir -p /usr/local/system_app_data/wallloop && cp config.ini wallloop.lang images/ 三件套` +
      `cp nginx/wallloop.conf /etc/nginx/conf.d/ && nginx -s reload` +
      `cp images/icons/wallloop.svg /usr/www/images/icons/`
- [ ] 启动台图标点开 → 悬浮窗显示管理面板(iframe,`/wallloop/`)
- [ ] 面板「演示壁纸生成」→ mandelbrot 5 秒 → 任务完成入库 → 出现在壁纸库
- [ ] 上传一张图片/一段视频 → 缩略图出现 → 设为正在播放
- [ ] 宿主机浏览器开 `http://169.254.104.128:18240/play` → 全屏播放器循环播放
- [ ] `curl http://169.254.104.128:18240/api/v1/now` 返回当前壁纸 JSON;`POST upload` 到公开面 → 404
- [ ] ffmpeg 实测为出厂自带:`/usr/bin/ffmpeg -version`
- [ ] `dpkg -P wallloop` 卸载无残留(用户/服务/`/usr/local/wallloop`/`/var/lib/wallloop`)
