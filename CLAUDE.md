# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DataCardPlugin is a LangBot V4.0 plugin for querying data/SIM card products from LLKShop. Users can search by price (e.g., "流量卡9元") or province (e.g., "流量卡广东"). The plugin scrapes product information from https://172.lot-ml.com and formats responses with images and product details.

## Architecture

### Plugin Structure (LangBot Plugin SDK)

This is a **LangBot plugin** that follows the LangBot Plugin SDK architecture:

- **Entry Point**: `main.py` defines `DataCardPlugin(BasePlugin)` - the main plugin class referenced in `manifest.yaml`
- **Event System**: Uses decorator-based event handlers (`@self.handler(events.GroupMessageReceived)`) in EventListener components
- **Component Loading**: EventListener components are defined in `components/event_listener/` with YAML manifests
- **Configuration**: Plugin config (like `llkshop_id`) is defined in `manifest.yaml` and accessed via `self.plugin.get_config()`

### Key Components

1. **main.py**: Minimal plugin initialization class (`DataCardPlugin`)
2. **components/event_listener/default.py**: Event handler that:
   - Listens for group messages matching pattern `^流量卡(.+)$`
   - Dynamically loads `core/datacard_search.py` using `importlib`
   - Parses markdown image syntax `![alt](url)` and converts to `platform_message.Image` objects
   - Builds message chains mixing text and images
3. **core/datacard_search.py**: Web scraper that:
   - Uses BeautifulSoup to parse product listings from LLKShop
   - Routes to different URL paths based on keyword type (province vs price/operator)
   - Deduplicates products by name and link
   - Returns structured dict with `success`, `results[]`, `shop_link`, etc.

### Message Flow

1. User sends "流量卡<keyword>" in group
2. `DefaultEventListener` regex matches and extracts keyword
3. Calls `search_data_cards(keyword, llkshop_id)` from dynamically loaded module
4. Scraper returns product data with markdown image syntax
5. Event handler parses markdown images with regex and builds `MessageChain`:
   - Text before image → `platform_message.Plain`
   - Image URL → `platform_message.Image`
   - Remaining text → `platform_message.Plain`
6. Sends via `event_context.reply(platform_message.MessageChain(...))`

## Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Required packages:
- `langbot-plugin` - LangBot Plugin SDK
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests

## Configuration

`manifest.yaml` defines:
- **llkshop_id**: Shop ID for LLKShop API (default: `3abcd2e80b9b4694`)
- Plugin metadata (version, author, description)
- Component paths (EventListener from `components/event_listener/`)

Users can override `llkshop_id` in their LangBot plugin settings.

## Important Implementation Notes

### Dynamic Module Loading
The plugin uses `importlib.util` to dynamically load `core/datacard_search.py` at runtime (see `default.py:41-45`). This is deliberate architecture - maintain this pattern when modifying the scraper.

### Image Message Handling
The scraper returns markdown image syntax (`![text](url)`), which the event handler parses with regex (`default.py:98-112`). When modifying image handling:
- Maintain markdown format in `datacard_search.py` output
- Keep regex pattern `r'!\[(.*?)\]\((http[s]?:\/\/[^)]+)\)'` in sync
- Preserve mixed Plain/Image message chain construction

### Keyword Routing Logic
`datacard_search.py:34-43` routes to different URL paths:
- Province keywords → `/producten/tyindex/{shop_id}`
- Price/operator keywords → `/ProductEn/Index/{shop_id}`

Modify this logic if LLKShop URL structure changes.

### Web Scraping Selectors
BeautifulSoup selectors (`default.py:58-89`) target specific HTML structure:
- Product containers: `div.new_lst`
- Product list items: `ul.fa > li`
- Product name: `h1`

These will break if the website HTML changes. Update selectors accordingly.

## Testing Locally

Since this is a LangBot plugin, testing requires the LangBot runtime environment. Refer to LangBot Plugin SDK documentation: https://docs.langbot.app/en/plugin/dev/tutor.html

## QQ Support Group

For issues and feature requests: QQ Group 965312424
