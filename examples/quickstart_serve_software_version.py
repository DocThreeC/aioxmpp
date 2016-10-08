########################################################################
# File name: quickstart_serve_software_version.py
# This file is part of: aioxmpp
#
# LICENSE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
########################################################################
import asyncio
import getpass

try:
    import readline  # NOQA
except ImportError:
    pass

import aioxmpp
import aioxmpp.xso as xso

namespace = "jabber:iq:version"


@aioxmpp.IQ.as_payload_class
class Query(xso.XSO):
    TAG = (namespace, "query")

    name = xso.ChildText(
        (namespace, "name"),
        default=None,
    )

    version = xso.ChildText(
        (namespace, "version"),
        default=None,
    )

    os = xso.ChildText(
        (namespace, "os"),
        default=None,
    )


async def handler(iq):
    print("software version request from {!r}".format(iq))
    result = Query()
    result.name = "aioxmpp Quick Start Pro"
    result.version = "23.42"
    result.os = "MFHBμKOS (My Fancy HomeBrew Micro Kernel Operating System)"
    return result


async def main(local_jid, password):
    client = aioxmpp.PresenceManagedClient(
        local_jid,
        aioxmpp.make_security_layer(password)
    )

    client.stream.register_iq_request_coro(
        "get",
        Query,
        handler,
    )

    async with client.connected():
        await asyncio.sleep(30)


if __name__ == "__main__":
    local_jid = aioxmpp.JID.fromstr(input("local JID> "))
    password = getpass.getpass()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(local_jid, password))
    loop.close()
