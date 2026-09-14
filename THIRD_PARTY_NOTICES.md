# Third-Party Notices

The Python implementation is distributed under the MIT license in LICENSE.
It is maintained independently by MintCandy and is not an official Decimal release.

Decimal transaction formats, endpoint mappings and interoperability behavior were
studied using the official Decimal SDKs:

- [dsc-js-sdk](https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/), including
  the endpoint map and EVM interface definitions. Reference revision: 6790d35.
- [dsc-go-sdk](https://bitbucket.org/decimalteam/dsc-go-sdk/src/master/).
- [dsc-python-sdk](https://bitbucket.org/decimalteam/dsc-python-sdk/src/master/),
  used as a documentation/workflow reference, not bundled as a dependency.

For incorporated/adapted material from dsc-js-sdk, retain its ISC notice:

Copyright (c) 2021, Crypton Studio

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Runtime dependencies (Web3.py, eth-account, aiohttp and python-dotenv) are installed
separately under their own licenses. No Go or JavaScript package, mobile project,
validator software, node database or wallet credentials are bundled.
