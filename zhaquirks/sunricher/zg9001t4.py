"""Sunricher ZG9001T4 device."""
import itertools
from zigpy.quirks import CustomDevice

from zigpy.profiles import zha
from zigpy.zcl.clusters.general import Basic, PowerConfiguration, Identify, Scenes, Groups, OnOff, LevelControl, GreenPowerProxy, Ota
from zigpy.zcl.clusters.lightlink import LightLink
from zigpy.zcl.clusters.lighting import Color
from zigpy.zcl.clusters.homeautomation import Diagnostic

from ..const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    TURN_OFF,
    TURN_ON,
    COMMAND,
    COMMAND_ON,
    COMMAND_OFF,
    COMMAND_STEP_ON_OFF,
    COMMAND_STEP_COLOR_TEMP,
    COMMAND_MOVE_ON_OFF,
    COMMAND_STOP,
    COMMAND_MOVE_TO_COLOR_TEMP,
    SET_COLOR_TEMP,
    ARGS,
    ALT_LONG_PRESS,
    ALT_DOUBLE_PRESS,
    LONG_RELEASE,
    DIM_UP,
    DIM_DOWN,
    DEVICE_TYPE,
    DOUBLE_PRESS,
    ENDPOINT_ID,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LONG_PRESS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    SHORT_PRESS,
    CLUSTER_ID
)


class SunricherZG9001T4(CustomDevice):
    """Sunricher ZG9001T4 device."""

    signature_endpoints = dict((x, {
        # SizePrefixedSimpleDescriptor(endpoint=1, profile=260, device_type=261, 
        # device_version=0, 
        # input_clusters=[0, 3, 2821, 4096], 
        # output_clusters=[3, 4, 5, 6, 8, 25, 768, 4096])
        PROFILE_ID: zha.PROFILE_ID,
        DEVICE_TYPE: zha.DeviceType.COLOR_DIMMER_SWITCH,
        INPUT_CLUSTERS: [
            Basic.cluster_id,
            Identify.cluster_id,
            Diagnostic.cluster_id,
            LightLink.cluster_id
        ],
        OUTPUT_CLUSTERS: [
            Identify.cluster_id,
            Groups.cluster_id,
            Scenes.cluster_id,
            OnOff.cluster_id,
            LevelControl.cluster_id,
            Ota.cluster_id,
            Color.cluster_id,
            LightLink.cluster_id
        ]
        }) for x in range(1, 5))
    
    # SizePrefixedSimpleDescriptor(endpoint=242, profile=41440, device_type=97, 
    # device_version=0, input_clusters=[], output_clusters=[33])
    signature_endpoints[242] = {
        PROFILE_ID: 41440,
        DEVICE_TYPE: 97,
        INPUT_CLUSTERS: [],
        OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id]
    }

    signature = {
        ENDPOINTS: signature_endpoints
    }

    replacementEndpoints = dict((x, {
        PROFILE_ID: zha.PROFILE_ID,
        DEVICE_TYPE: zha.DeviceType.COLOR_DIMMER_SWITCH,
        INPUT_CLUSTERS: [
            Basic.cluster_id,
            Identify.cluster_id,
            Diagnostic.cluster_id,
            LightLink.cluster_id
        ],
        OUTPUT_CLUSTERS: [
            Identify.cluster_id,
            Groups.cluster_id,
            Scenes.cluster_id,
            OnOff.cluster_id, # PhilipsOnOffCluster
            LevelControl.cluster_id, # PhilipsLevelControlCluster
            Ota.cluster_id,
            Color.cluster_id, # PhilipsColorCluster
            LightLink.cluster_id
        ]
        }) for x in range(1, 5))

    replacementEndpoints[242] = {
        PROFILE_ID: 41440,
        DEVICE_TYPE: 97,
        INPUT_CLUSTERS: [],
        OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id]
    }


    replacement = {
        ENDPOINTS: replacementEndpoints
    }
    
    buttons = [BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4]

    device_automation_triggers = dict(itertools.chain([itertools.chain([
        ((btn, TURN_ON), {COMMAND: COMMAND_ON, CLUSTER_ID: 6, ENDPOINT_ID: i + 1}),
        ((btn, TURN_OFF), {COMMAND: COMMAND_OFF, CLUSTER_ID: 6, ENDPOINT_ID: i + 1}),
        ((btn, DIM_UP), {COMMAND: COMMAND_STEP_ON_OFF, CLUSTER_ID: 8, ENDPOINT_ID: i + 1, ARGS: [0, 32, 0]}),
        ((btn, DIM_DOWN), {COMMAND: COMMAND_STEP_ON_OFF, CLUSTER_ID: 8, ENDPOINT_ID: i + 1, ARGS: [1, 32, 0]}),
        ((btn, LONG_PRESS), {COMMAND: COMMAND_MOVE_ON_OFF, CLUSTER_ID: 8, ENDPOINT_ID: i + 1, ARGS: [0, 50]}), # increase brightness
        ((btn, SHORT_PRESS), {COMMAND: COMMAND_MOVE_ON_OFF, CLUSTER_ID: 8, ENDPOINT_ID: i + 1, ARGS: [1, 50]}), # decrease brightness
        ((btn, LONG_RELEASE), {COMMAND: COMMAND_STOP, CLUSTER_ID: 8, ENDPOINT_ID: i + 1}), ## stop increasing/decreasing brightness
        ((btn, SET_COLOR_TEMP), {COMMAND: COMMAND_MOVE_TO_COLOR_TEMP, CLUSTER_ID: 768, ENDPOINT_ID: i + 1}),
        ((btn, ALT_DOUBLE_PRESS), {COMMAND: "recall", CLUSTER_ID: 5, ENDPOINT_ID: i + 1}), ## scene button short press
        ((btn, ALT_LONG_PRESS), {COMMAND: "store", CLUSTER_ID: 5, ENDPOINT_ID: i + 1}), ## scene button long press
        ])
    for i, btn in enumerate(buttons)
    ]))
