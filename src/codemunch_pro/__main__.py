"""CLI entry point for CodeMunch Pro."""

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='codemunch-pro',
        description='Intelligent code indexing MCP server',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s 0.1.0',
    )
    parser.add_argument(
        '--transport',
        choices=['stdio', 'streamable-http'],
        default='stdio',
        help='MCP transport (default: stdio)',
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5002,
        help='Port for streamable-http transport (default: 5002)',
    )

    args = parser.parse_args()

    from codemunch_pro.server import create_server

    mcp = create_server(transport=args.transport, port=args.port)

    if args.transport == 'stdio':
        mcp.run(transport='stdio')
    else:
        mcp.run(
            transport='streamable-http',
            host='0.0.0.0',
            port=args.port,
        )


if __name__ == '__main__':
    main()
