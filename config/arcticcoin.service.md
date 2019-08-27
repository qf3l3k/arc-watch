# Service file

Location: /lib/systemd/system/arcticcoind.service

```apache
[Unit]
Description=Arctic Coin Service
After=network.target

[Service]
User=root
Group=root
Type=forking
PIDFile=/root/.arcticcore/arcticcoind.pid
ExecStart=/usr/local/bin/arcticcoind -daemon -conf=/root/.arcticcore/arcticcoin.conf -datadir=/root/.arcticcore
ExecStop=/usr/local/bin/arcticcoin-cli -conf=/root/.arcticcore/arcticcoin.conf -datadir=/root/.arcticcore stop
Restart=always
PrivateTmp=true
TimeoutStopSec=60s
TimeoutStartSec=10s
StartLimitInterval=120s
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
Alias=arcticcoind.service
```

# Enable service
```bash
systemctl enable /lib/systemd/system/arcticcoind.service
```