---
title: SONOS/SYMFONISK Examples
layout: page
---

### SONOS/SYMFONISK single speaker

ControllerX can 'out of the box' control single speakers with following small app setup.
Supports:

- Toggle play/pause, volume up/down, previous/next song (in playlist) and previous/next favourites from Sonos app (source list).

This favourites list can consist of both radio stations, playlists, podcasts etc. Source list is 'circular'. Meaning that choosing next when at last source in list, will skip to first source in list - and vice versa.

```yaml
office_sonos_controller:
  module: controllerx
  class: E1810MediaPlayerController
  controller: sensor.controller_action
  integration: z2m
  volume_steps: 20 # default setting is 10. This will increase default steps to 20 from no volume to full volume
  media_player: media_player.office
```

### SONOS/SYMFONISK groups

ControllerX supports Sonos groups as well. If media_player in app is set to a group, then ControllerX will read the Sonos source list from FIRST entity_id in group. So this has to be your chosen master speaker! This setup will work perfectly, if you only use static groups that are never altered (via Sonos app/HA or otherwise). But if your Sonos group alters through the day (other family members redefines group speakers to their liking), you need a dynamic group setting.

This can easily be achieved by adding only one sensor and one small automation to your HA configuration.

#### HA configuration.yaml

{% assign special = "{{ state_attr('media_player.office', 'sonos_group') }}" %}

```yaml
- platform: template
  sensors:
    sonos_master_group_entities:
        value_template: "{{ special }}" #MASTER speaker
```

#### HA automation.yaml

{% assign special = "{{ state_attr('media_player.office', 'sonos_group') | join(',') }}" %}

```yaml
id: dynamic_sonos_groups
alias: dynamic_sonos_groups
trigger:
  platform: state
  entity_id: sensor.sonos_master_group_entities # Same as defined in configuration.yaml
action:
  - service: group.set
    data_template:
      object_id: sonos_all #name of sonos group in groups.yaml
      entities: "{{ special }}" #MASTER speaker
```

#### HA groups.yaml

```yaml
name: sonos_all
entities:
  - media_player.office #this HAS to be your MASTER speaker
  - media_player.kitchen #SLAVE speaker #1
  - media_player.livingroom #SLAVE speaker #2
```

And with the following ControllerX configuration, you will be able to control the dynamic group in HA, which will be changed immediately if group is altered eg. from Sonos app. This app version below, has 'flipped' the arrow functions. So click will change source and hold will change previous/next song in playlist. This behaviour will most likely fit better for users that primarily uses favourites (radio stations).

#### Appdeamon apps.yaml

```yaml
sonos_group:
  module: controllerx
  class: CustomMediaPlayerController
  controller: sensor.controller_action
  integration: z2m
  volume_steps: 20
  media_player: group.sonos_all #Sonos group in groups.yaml
  mapping:
    toggle: play_pause
    brightness_up_click: click_volume_up
    brightness_down_click: click_volume_down
    brightness_up_hold: hold_volume_up
    brightness_down_hold: hold_volume_down
    brightness_up_release: release
    brightness_down_release: release
    arrow_right_click: next_source
    arrow_left_click: previous_source
    arrow_right_hold: next_track
    arrow_left_hold: previous_track
```
