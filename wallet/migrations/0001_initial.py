# Generated by Django 4.1.1 on 2022-11-15 02:27

import common.models
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "index",
                    models.CharField(
                        db_index=True, max_length=10, verbose_name="address index"
                    ),
                ),
                ("address", models.CharField(max_length=70, verbose_name="address")),
            ],
            options={
                "verbose_name": "address",
                "verbose_name_plural": "address",
            },
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "device_id",
                    models.CharField(max_length=70, verbose_name="device id"),
                ),
                (
                    "wallet_uuid",
                    models.CharField(max_length=70, verbose_name="wallet uuid"),
                ),
                (
                    "wallet_name",
                    models.CharField(max_length=70, verbose_name="wallet name"),
                ),
                (
                    "asset_usd",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="total usd",
                    ),
                ),
                (
                    "asset_cny",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="total cny",
                    ),
                ),
                (
                    "chain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallet_chain",
                        to="common.chain",
                        verbose_name="chain",
                    ),
                ),
            ],
            options={
                "verbose_name": "wallet",
                "verbose_name_plural": "wallet",
            },
        ),
        migrations.CreateModel(
            name="WalletHead",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "wallet_head",
                    models.CharField(max_length=512, verbose_name="wallethead"),
                ),
                ("rsa_public_key", models.TextField(verbose_name="rsa public key")),
                ("rsa_private_key", models.TextField(verbose_name="rsa private key")),
                ("ipfs_cid", models.CharField(max_length=128, verbose_name="ipfs cid")),
                (
                    "wallet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wallet.wallet",
                        verbose_name="wallet",
                    ),
                ),
            ],
            options={
                "verbose_name": "WalletHead",
                "verbose_name_plural": "WalletHead",
            },
        ),
        migrations.CreateModel(
            name="WalletAsset",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "contract_addr",
                    models.CharField(max_length=70, verbose_name="contract address"),
                ),
                (
                    "asset_usd",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="wallet usd",
                    ),
                ),
                (
                    "asset_cny",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="wallet cny",
                    ),
                ),
                (
                    "balance",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="wallet balance",
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallet_asset_asset",
                        to="common.asset",
                        verbose_name="asset",
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wallet_asset_wallet",
                        to="wallet.wallet",
                        verbose_name="wallet",
                    ),
                ),
            ],
            options={
                "verbose_name": "wallet_asset",
                "verbose_name_plural": "wallet_asset",
            },
        ),
        migrations.CreateModel(
            name="TxRecord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("from_addr", models.CharField(max_length=70, verbose_name="发送方")),
                ("to_addr", models.CharField(max_length=70, verbose_name="接收方")),
                (
                    "amount",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="转账金额",
                    ),
                ),
                ("memo", models.CharField(max_length=70, verbose_name="备注")),
                ("hash", models.CharField(max_length=70, verbose_name="交易Hash")),
                ("block_height", models.CharField(max_length=70, verbose_name="所在区块")),
                ("tx_time", models.CharField(max_length=70, verbose_name="交易时间")),
                (
                    "asset",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.asset",
                        verbose_name="资产名称",
                    ),
                ),
                (
                    "chain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.chain",
                        verbose_name="链名称",
                    ),
                ),
            ],
            options={
                "verbose_name": "交易记录表",
                "verbose_name_plural": "交易记录表",
            },
        ),
        migrations.CreateModel(
            name="TokenConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "token_name",
                    models.CharField(max_length=70, verbose_name="token 名称"),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True, null=True, upload_to="wallet/%Y/%m/%d/"
                    ),
                ),
                (
                    "token_symbol",
                    models.CharField(max_length=70, verbose_name="Token符号"),
                ),
                ("contract_addr", models.CharField(max_length=70, verbose_name="合约地址")),
                (
                    "decimal",
                    models.CharField(
                        db_index=True, max_length=10, verbose_name="token 精度"
                    ),
                ),
                (
                    "is_hot",
                    models.CharField(
                        choices=[("yes", "yes"), ("no", "no")],
                        default="no",
                        max_length=32,
                        verbose_name="是不是热门资产",
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.asset",
                        verbose_name="资产名称",
                    ),
                ),
                (
                    "chain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.chain",
                        verbose_name="链名称",
                    ),
                ),
            ],
            options={
                "verbose_name": "资产配置表",
                "verbose_name_plural": "资产配置表",
            },
        ),
        migrations.CreateModel(
            name="AddressAsset",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "asset_usd",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="address usd",
                    ),
                ),
                (
                    "asset_cny",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="address cny",
                    ),
                ),
                (
                    "balance",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="address balance",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address_asset_address",
                        to="wallet.address",
                        verbose_name="address",
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address_asset_asset",
                        to="common.asset",
                        verbose_name="asset",
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address_asset_wallet",
                        to="wallet.wallet",
                        verbose_name="wallet",
                    ),
                ),
            ],
            options={
                "verbose_name": "AddressAsset",
                "verbose_name_plural": "AddressAsset",
            },
        ),
        migrations.CreateModel(
            name="AddressAmountStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "amount",
                    common.models.DecField(
                        decimal_places=30,
                        default=Decimal("0E-18"),
                        max_digits=65,
                        verbose_name="amount",
                    ),
                ),
                ("timedate", models.CharField(max_length=70, verbose_name="timedate")),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wallet.address",
                        verbose_name="address",
                    ),
                ),
            ],
            options={
                "verbose_name": "AddressAmountStat",
                "verbose_name_plural": "AddressAmountStat",
            },
        ),
        migrations.AddField(
            model_name="address",
            name="wallet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wallet_address",
                to="wallet.wallet",
                verbose_name="wallet",
            ),
        ),
        migrations.CreateModel(
            name="AddresNote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("device_id", models.CharField(max_length=70, verbose_name="设备ID")),
                ("memo", models.CharField(max_length=70, verbose_name="地址备注")),
                ("address", models.CharField(max_length=70, verbose_name="地址")),
                (
                    "asset",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.asset",
                        verbose_name="资产名称",
                    ),
                ),
                (
                    "chain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.chain",
                        verbose_name="链名称",
                    ),
                ),
            ],
            options={
                "verbose_name": "地址薄表",
                "verbose_name_plural": "地址薄表",
            },
        ),
    ]
