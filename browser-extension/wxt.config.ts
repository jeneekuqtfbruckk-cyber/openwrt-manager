import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'OpenWrt Manager',
    description: 'Lightweight OpenWrt management assistant',
    version: '0.1.0',
    icons: {
      "16": "icon-16.png",
      "32": "icon-32.png",
      "48": "icon-48.png",
      "128": "icon-128.png"
    },
    action: {
      default_title: "OpenWrt Manager",
      default_popup: "popup.html",
      default_icon: {
        "16": "icon-16.png",
        "32": "icon-32.png",
        "48": "icon-48.png",
        "128": "icon-128.png"
      }
    },
    permissions: [
      'storage',
      'tabs',
      'scripting'
    ],
    // Chrome MV3 prohibits IP wildcards like '192.168.*.*'.
    // To support ANY internal/external IP or Domain, we must request broad access.
    host_permissions: [
      'http://*/*',
      'https://*/*',
      '<all_urls>'
    ],
    commands: {
      "wxt:reload-extension": {
        "description": "Reload the extension during development",
        "suggested_key": {
          "default": "Alt+R"
        }
      }
    },
    content_security_policy: {
      extension_pages: "script-src 'self' 'wasm-unsafe-eval' http://localhost:3000; object-src 'self';",
      sandbox: "script-src 'self' 'unsafe-inline' 'unsafe-eval' http://localhost:3000; sandbox allow-scripts allow-forms allow-popups allow-modals; child-src 'self';"
    }
  },
});
