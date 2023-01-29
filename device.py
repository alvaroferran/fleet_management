from dataclasses import dataclass


@dataclass
class Device:
    """Device data class

    Args:
        device_id (int): Device identifier.
        alias (str): Human-readable device name.
        client (str): Client where the device is installed.
        payment_required (bool): Is payment expected. Defaults to "True".
    """

    device_id: int = 0
    alias: str = ""
    client: str = ""
    payment_required: bool = True
