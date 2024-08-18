<br/>
<p align="center">
  <a href="https://github.com/VatosV2/Discord-Gen-Bot">
    <img src="https://nexustools.de/Assets/images/025111e73c9100f75a2f4adfc06161df.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">[Nexus Gen Bot] - discord.gg/nexustools</h3>

  <p align="center">
    Nexus Gen bot - Take your Gen server to the Next level.
    <br/>
    <br/>
    <a href="https://discord.gg/nexustools">Discord</a>
  </p>
</p>
<h3 align="center";">Please Star To support this project for free! ⭐</h3>
<h3 align="center";">Linux is Supported! ✅</h3>
<br/>
<h3 align="center";>  https://nexustools.de/ </h3>

## Screenshot
![ss](https://repository-images.githubusercontent.com/803993834/39e7da65-32b2-49cc-b832-fce6f563eae0)

## Release
- 25 Stars For Release ⭐ ✅
- 50 Stars For V2 ⭐ ❌

## Functions
```yaml
/add_service {gen_type} {service} {file(optional)} ✅ 

/gen                         ✅
/booster_gen                 ✅
/premium_gen                 ✅

/stock                       ✅    
/booster_stock               ✅
/premium_stock               ✅

/restock_free_gen            ✅
/restock_booster_gen         ✅
/restock_premium_gen         ✅

/remove_free_service         ✅
/remove_booster_service      ✅
/remove_premium_service      ✅

/clear_free_stock            ✅
/clear_booster_stock         ✅
/clear_premium_stock         ✅

/whitelist                   ✅
/unwhitelist                 ✅
/get_log_file                ✅

Free Gen If Vanity in status ✅
Status Change Logs           ✅
Logs                         ✅

```

## Config
```json
{
    "bot_token": "bot_token",
    "owner_id": 1234567891011121134,
    "server_id": 1234567891011121134,
    "bot_status": "discord.gg/nexustools",
    "free_gen": {
        "free_gen_role": 1234567891011121134,
        "free_gen_channel": 1234567891011121134,
        "free_gen_status": "discord.gg/nexustools",
        "status_log_channel": 1234567891011121134,
        "free_gen_cooldown": 120,
        "free_gen_folder": "stocks/stock"
    },
    "boost_gen": {
        "boost_gen_role": 1234567891011121134,
        "boost_gen_channel": 1234567891011121134,
        "boost_gen_cooldown": 60,
        "boost_gen_folder": "stocks/boost_gen_stock"
    },
    "premium_gen": {
        "premium_gen_role": 1234567891011121134,
        "premium_gen_channel": 1234567891011121134,
        "premium_gen_cooldown": 120,
        "premium_gen_folder": "stocks/premium_gen_stock"
    },
    "logs": {
        "free_gen_log_webhook": "Discord Webhook To log Free gen",
        "booster_gen_log_webhook": "Discord Webhook To log booster gen",
        "premium_gen_log_webhook": "Discord Webhook To log premium gen",
        "admin_commands_log_webhook": "Discord Webhook To log admin commands"
    }
} 
```
