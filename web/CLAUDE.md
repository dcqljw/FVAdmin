# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FVAdmin is a Vue 3 admin panel built on the Art Design Pro framework, featuring TypeScript, Element Plus, Tailwind CSS, and Pinia for state management.

## Commands

```bash
# Development
pnpm dev                    # Start dev server (Vite)

# Build
pnpm build                  # Type check and build for production

# Linting
pnpm lint                   # Run ESLint
pnpm fix                    # Auto-fix ESLint issues
pnpm lint:prettier          # Format with Prettier
pnpm lint:stylelint         # Fix style issues with Stylelint

# Other
pnpm commit                 # Commit with conventional commit format (git-cz)
pnpm clean:dev              # Clean dev artifacts
```

## Architecture Overview

### Core Structure

```
src/
├── api/              # API functions (axios wrapper in utils/http)
├── components/       # Reusable components
│   └── core/         # Framework-level components (layouts, tables, forms, etc.)
├── config/           # System configuration (theme, menu, colors)
├── directives/       # Custom Vue directives
├── enums/            # TypeScript enums
├── hooks/            # Composables (useAuth, useTable, useTheme, etc.)
├── locales/          # i18n translations (zh/en via vue-i18n)
├── router/           # Vue Router with dynamic routes from backend
├── store/            # Pinia stores with persistence
├── types/            # TypeScript type definitions
├── utils/            # Utility functions
└── views/            # Page components
```

### Key Patterns

**Path Aliases** (defined in `vite.config.ts` and `tsconfig.json`):
- `@` → `src/`
- `@views` → `src/views/`
- `@utils` → `src/utils/`
- `@stores` → `src/store/`
- `@styles` → `src/assets/styles/`
- `@imgs`, `@icons` → asset directories

**Auto-Imports** (via unplugin-auto-import):
Vue, Vue Router, Pinia, VueUse, and Element Plus APIs are auto-imported. No need to import `ref`, `computed`, `ElMessage`, etc.

**API Type Definitions**:
Use the global `Api` namespace (defined in `src/types/api/api.d.ts`):
```typescript
const params: Api.Auth.LoginParams = { username: 'admin', password: '123456' }
const response: Api.SystemManage.UserList = await fetchGetUserList(params)
```

**HTTP Client** (`src/utils/http/index.ts`):
- Based on Axios with request/response interceptors
- Auto-attaches Authorization header from user store
- Handles 401 errors with auto-logout (debounced)
- Supports retry logic for server errors
- Usage: `import request from '@/utils/http'`

**Routing**:
- Static routes (`src/router/routes/staticRoutes.ts`): Login, error pages, iframe
- Dynamic routes: Loaded from backend API after login
- Route guards (`src/router/guards/`): Handle auth, permission checks, dynamic registration
- Hash-based routing (`createWebHashHistory`)

**State Management** (Pinia with persistedstate):
- Stores: `user`, `menu`, `setting`, `worktab`, `table`
- Persisted to localStorage with versioned keys: `sys-v{version}-{storeId}`
- Access stores: `import { useUserStore } from '@/store/modules/user'`

**Internationalization**:
- Languages: Chinese (zh), English (en)
- Use `$t('key')` globally or `useI18n()` in components
- Language files: `src/locales/langs/zh.json` and `en.json`

## Environment Variables

Defined in `.env.development` and `.env.production`:
- `VITE_API_URL`: API base URL
- `VITE_API_PROXY_URL`: Proxy target for dev server
- `VITE_BASE_URL`: App deployment base path
- `VITE_VERSION`: App version

## Code Style

- **ESLint**: Flat config (`eslint.config.mjs`) with TypeScript and Vue support
- **Prettier**: Code formatting
- **Stylelint**: CSS/SCSS/Vue style linting
- **Commitlint**: Conventional commits enforced via Husky hooks
- **Quotes**: Single quotes
- **Semicolons**: No semicolons
- **Lint-staged**: Auto-runs on commit for `*.{js,ts,vue}` files

## SCSS Setup

Global SCSS imports (via `vite.config.ts`):
```scss
@use "@styles/core/el-light.scss" as *;
@use "@styles/core/mixin.scss" as *;
```

These are available in all Vue component `<style lang="scss">` blocks without explicit import.
