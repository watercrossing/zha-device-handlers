from zigpy.quirks import CustomDevice

from zigpy.profiles import zha
from zigpy.zcl.clusters.general import Basic, PowerConfiguration, Identify, Scenes, Groups, OnOff, LevelControl, GreenPowerProxy
from zigpy.zcl.clusters.lightlink import LightLink
from zigpy.zcl.clusters.lighting import Color

from ..const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    COMMAND,
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
)


class SunricherZG9001T4(CustomDevice):
    """Sunricher ZG9001T4 device."""

    signature_endpoints = dict((x, {
        # SizePrefixedSimpleDescriptor(endpoint=1, profile=260, device_type=261, 
        # device_version=0, 
        # input_clusters=[0, 3, 2821, 4096], 
        # output_clusters=[3, 4, 5, 6, 8, 25, 768, 4096])
        ROFILE_ID: zha.PROFILE_ID,
        DEVICE_TYPE: zha.DeviceType.COLOR_DIMMER_SWITCH,
        INPUT_CLUSTERS: [
            Basic.cluster_id,
            PowerConfiguration.cluster_id,
            Identify.cluster_id,
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
            PowerConfiguration.cluster_id,
            Identify.cluster_id,
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
