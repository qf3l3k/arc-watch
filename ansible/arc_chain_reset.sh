#!/bin/bash
service arcticcoind stop
rm -rf /root/.arcticcore/arcticcoind.pid
rm -rf /root/.arcticcore/backups
rm -rf /root/.arcticcore/banlist.dat
rm -rf /root/.arcticcore/blocks
rm -rf /root/.arcticcore/chainstate
rm -rf /root/.arcticcore/database
rm -rf /root/.arcticcore/db.log
rm -rf /root/.arcticcore/debug.log
rm -rf /root/.arcticcore/fee_estimates.dat
rm -rf /root/.arcticcore/gmcache.dat
rm -rf /root/.arcticcore/gmpayments.dat
rm -rf /root/.arcticcore/governance.dat
rm -rf /root/.arcticcore/netfulfilled.dat
rm -rf /root/.arcticcore/peers.dat
tar -xvf /root/.arcticcore/chain_arc_201906071139.tar -C /root/.arcticcore
service arcticcoind start
