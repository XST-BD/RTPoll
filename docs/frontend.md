# Frontend Documentation

> **Last Updated:** June 25, 2026

## Table of Contents

- [Frontend Documentation](#frontend-documentation)
  - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. Technology Stack](#2-technology-stack)
  - [3. Project Structure](#3-project-structure)
  - [4. Environment \& Configuration](#4-environment--configuration)
    - [4.1 Environment Variables](#41-environment-variables)
    - [4.2 Nuxt Configuration](#42-nuxt-configuration)
  - [5. Root Application Files](#5-root-application-files)
    - [5.1 app.vue — Root Component](#51-appvue--root-component)
    - [5.2 error.vue — Global Error Page](#52-errorvue--global-error-page)
  - [6. Styling \& Design System](#6-styling--design-system)
    - [6.1 Typography](#61-typography)
    - [6.2 Color Palette](#62-color-palette)
    - [6.3 Button System](#63-button-system)
    - [6.4 Link System](#64-link-system)
    - [6.5 Form Elements](#65-form-elements)
    - [6.6 Utility Classes](#66-utility-classes)
  - [7. Layouts](#7-layouts)
    - [7.1 Default Layout](#71-default-layout)
    - [7.2 marketing.vue](#72-marketingvue)
    - [7.3 dashboard.vue](#73-dashboardvue)
    - [7.4 mail-redirect.vue](#74-mail-redirectvue)
  - [8. Middleware](#8-middleware)
    - [8.1 auth.js](#81-authjs)
    - [8.2 guest.js](#82-guestjs)
  - [9. Composables](#9-composables)
    - [9.1 useApi](#91-useapi)
    - [9.2 useAuth](#92-useauth)
    - [9.3 usePopup](#93-usepopup)
    - [9.4 useValidation](#94-usevalidation)
    - [9.5 usePollToken](#95-usepolltoken)
    - [9.6 useWebSocket](#96-usewebsocket)
  - [10. Plugins](#10-plugins)
    - [10.1 apexcharts.client.js](#101-apexchartsclientjs)
  - [11. Utilities](#11-utilities)
    - [11.1 formatNumber](#111-formatnumber)
  - [12. Pages (Routing)](#12-pages-routing)
    - [12.1 Route Map](#121-route-map)
    - [12.2 Public Pages](#122-public-pages)
      - [`pages/index.vue` — Landing Page](#pagesindexvue--landing-page)
      - [`pages/about.vue` — About Page](#pagesaboutvue--about-page)
    - [12.3 Authentication Pages](#123-authentication-pages)
      - [`pages/login.vue` — Login Page](#pagesloginvue--login-page)
      - [`pages/register.vue` — Registration Page](#pagesregistervue--registration-page)
    - [12.4 Email Action Pages](#124-email-action-pages)
      - [`pages/verify-mail.vue` — Email Verification](#pagesverify-mailvue--email-verification)
      - [`pages/update-mail.vue` — Email Change Confirmation](#pagesupdate-mailvue--email-change-confirmation)
      - [`pages/recover-pass.vue` — Password Reset](#pagesrecover-passvue--password-reset)
    - [12.5 Dashboard Pages (Authenticated)](#125-dashboard-pages-authenticated)
      - [`pages/dashboard/index.vue` — Dashboard Home](#pagesdashboardindexvue--dashboard-home)
      - [`pages/dashboard/create.vue` — Create Poll](#pagesdashboardcreatevue--create-poll)
      - [`pages/dashboard/settings.vue` — User Settings](#pagesdashboardsettingsvue--user-settings)
      - [`pages/dashboard/poll/[id].vue` — Poll Detail (Creator View)](#pagesdashboardpollidvue--poll-detail-creator-view)
    - [12.6 Public Poll Voter Page](#126-public-poll-voter-page)
      - [`pages/poll/[id].vue` — Public Voting Page](#pagespollidvue--public-voting-page)
    - [12.7 Placeholder Pages](#127-placeholder-pages)
  - [13. Components](#13-components)
    - [13.1 Component Hierarchy](#131-component-hierarchy)
    - [13.2 Marketing Components](#132-marketing-components)
      - [`marketing/Navbar.vue`](#marketingnavbarvue)
      - [`marketing/Footer.vue`](#marketingfootervue)
    - [13.3 Dashboard Navigation Components](#133-dashboard-navigation-components)
      - [`FloatingNavPanel.vue`](#floatingnavpanelvue)
      - [`LogoutBtn.vue`](#logoutbtnvue)
    - [13.4 Notification Components](#134-notification-components)
      - [`PopupMessage.vue`](#popupmessagevue)
    - [13.5 Poll Display Components](#135-poll-display-components)
      - [`PollCard.vue`](#pollcardvue)
      - [`RunningPollView.vue`](#runningpollviewvue)
      - [`ClosedPollView.vue`](#closedpollviewvue)
      - [`GraphView.vue`](#graphviewvue)
      - [`PollSettings.vue`](#pollsettingsvue)
    - [13.6 Settings Components](#136-settings-components)
      - [`ChangeEmail.vue`](#changeemailvue)
      - [`ChangePassword.vue`](#changepasswordvue)
      - [`DeleteAccountBtn.vue`](#deleteaccountbtnvue)
      - [`DeleteAllPollBtn.vue`](#deleteallpollbtnvue)
      - [`DeleteClosedPollBtn.vue`](#deleteclosedpollbtnvue)
    - [13.7 Shared UI Components](#137-shared-ui-components)
      - [`Loading.vue`](#loadingvue)
      - [`PoweredByFooter.vue`](#poweredbyfootervue)
      - [`ProfileCard.vue`](#profilecardvue)
      - [`ForgotPasswordWindow.vue`](#forgotpasswordwindowvue)
  - [14. State Management](#14-state-management)
  - [15. Authentication Architecture](#15-authentication-architecture)
    - [15.1 Token Strategy](#151-token-strategy)
    - [15.2 Cross-Tab Synchronization](#152-cross-tab-synchronization)
    - [15.3 Auto-Refresh Mechanism](#153-auto-refresh-mechanism)
    - [15.4 Auth Flow Diagrams](#154-auth-flow-diagrams)
  - [16. Real-Time Architecture (WebSocket)](#16-real-time-architecture-websocket)
    - [16.1 Connection Flow](#161-connection-flow)
    - [16.2 Poll Token System](#162-poll-token-system)
    - [16.3 Message Protocol](#163-message-protocol)
    - [16.4 Reconnection Strategy](#164-reconnection-strategy)
  - [17. API Integration](#17-api-integration)
    - [17.1 Endpoint Map](#171-endpoint-map)
    - [17.2 Error Handling](#172-error-handling)
  - [18. SEO \& Meta Configuration](#18-seo--meta-configuration)
  - [19. Static Assets](#19-static-assets)
  - [20. Build \& Deployment](#20-build--deployment)
    - [20.1 Scripts](#201-scripts)
    - [20.2 SSR Strategy](#202-ssr-strategy)
    - [20.3 Deployment Target](#203-deployment-target)
  - [21. Development Guide](#21-development-guide)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Local Development](#local-development)
    - [Production Build](#production-build)
    - [Git Ignore Rules](#git-ignore-rules)

## 1. Overview

**RTPoll** is a real-time polling platform that allows authenticated users to create polls, share them via public links, and track live voting results through an interactive dashboard with charts, countdown timers, and WebSocket-powered live updates. Anonymous voters can participate without needing an account.

Key capabilities of the frontend:

- **Real-time vote tracking** via WebSocket connections
- **Browser fingerprinting** to prevent duplicate votes
- **Multi-tab authentication synchronization** via `BroadcastChannel`
- **JWT-based access tokens** stored in-memory for XSS protection
- **Hybrid SSR / CSR rendering** with per-route configuration
- **Cloudflare Pages** deployment target

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| [Nuxt.js](https://nuxt.com/) | Vue.js meta-framework (SSR, routing, auto-imports) |
| [Vue.js](https://vuejs.org/) | Reactive UI framework |
| [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework |
| [ApexCharts](https://apexcharts.com/)  | Interactive charting library |
| [FingerprintJS](https://fingerprintjs.com/) | Browser fingerprinting library |
| [Iconify for Vue](https://iconify.design/) | Universal icon framework |
| [vue3-flip-countdown](https://github.com/coskuncay/vue3-flip-countdown) | Animated flip-style countdown timer |
| [pnpm](https://pnpm.io/) | Package manager |

## 3. Project Structure

```
frontend/
├── .env.example                      # Example environment variables to copy to .env (API & WebSocket URLs)
├── .gitignore                        # Git ignore rules
├── nuxt.config.ts                    # Nuxt framework configuration
├── package.json                      # Dependencies and scripts
├── pnpm-lock.yaml                    # Lockfile
├── pnpm-workspace.yaml               # pnpm workspace settings
├── tsconfig.json                     # TypeScript configuration
├── README.md                         # Default Nuxt readme
│
├── app/                              # Application source code
│   ├── app.vue                       # Root application component
│   ├── error.vue                     # Global error page (404, 500, etc.)
│   │
│   ├── assets/
│   │   └── css/
│   │       └── global.css            # Global styles, design tokens, reusable classes
│   │
│   ├── components/
│   │   ├── marketing/
│   │   │   ├── Navbar.vue            # Marketing site navigation bar
│   │   │   └── Footer.vue            # Marketing site footer
│   │   ├── ChangeEmail.vue           # Email change form with confirmation modal
│   │   ├── ChangePassword.vue        # Password change form
│   │   ├── ClosedPollView.vue        # Paginated closed polls list
│   │   ├── DeleteAccountBtn.vue      # Account deletion with password confirmation
│   │   ├── DeleteAllPollBtn.vue      # Bulk delete all polls
│   │   ├── DeleteClosedPollBtn.vue   # Bulk delete expired polls only
│   │   ├── FloatingNavPanel.vue      # Fixed bottom navigation dock (dashboard)
│   │   ├── ForgotPasswordWindow.vue  # Forgot password modal dialog
│   │   ├── GraphView.vue             # Vote history bar chart (ApexCharts)
│   │   ├── Loading.vue               # Animated loading spinner
│   │   ├── LogoutBtn.vue             # Logout icon button
│   │   ├── PollCard.vue              # Poll summary card (question, top pick, votes, expiry)
│   │   ├── PollSettings.vue          # Poll settings dropdown with delete action
│   │   ├── PopupMessage.vue          # Toast notification stack
│   │   ├── PoweredByFooter.vue       # Minimal branded footer
│   │   ├── ProfileCard.vue           # Team member profile card
│   │   └── RunningPollView.vue       # Paginated active polls list
│   │
│   ├── composables/
│   │   ├── useApi.js                 # HTTP client wrapper around $fetch
│   │   ├── useAuth.js                # Authentication state & operations
│   │   ├── usePopup.js               # Toast notification state & helpers
│   │   ├── useValidation.js          # Form validation helpers
│   │   ├── usePollToken.js           # Poll-scoped JWT token management
│   │   └── useWebSocket.js           # WebSocket connection manager
│   │
│   ├── layouts/
│   │   ├── dashboard.vue             # Authenticated dashboard shell
│   │   ├── mail-redirect.vue         # Minimal centered layout for email actions
│   │   └── marketing.vue             # Public marketing site shell
│   │
│   ├── middleware/
│   │   ├── auth.js                   # Requires authentication (redirects to login)
│   │   └── guest.js                  # Blocks authenticated users (redirects to dashboard)
│   │
│   ├── pages/
│   │   ├── index.vue                 # Landing / marketing home page
│   │   ├── about.vue                 # About Us with team profiles
│   │   ├── login.vue                 # Login form
│   │   ├── register.vue              # Registration form
│   │   ├── recover-pass.vue          # Password reset (from email link)
│   │   ├── verify-mail.vue           # Email verification (from email link)
│   │   ├── update-mail.vue           # Email change confirmation (from email link)
│   │   ├── contact.vue               # Contact page (placeholder)
│   │   ├── privacy-policy.vue        # Privacy policy (placeholder)
│   │   ├── poll/
│   │   │   └── [id].vue              # Public poll voting page (anonymous)
│   │   └── dashboard/
│   │       ├── index.vue             # Dashboard home — running & closed polls
│   │       ├── create.vue            # Create new poll form
│   │       ├── settings.vue          # User settings & danger zone
│   │       └── poll/
│   │           └── [id].vue          # Poll detail view (creator, with live updates)
│   │
│   ├── plugins/
│   │   └── apexcharts.client.js      # Client-side ApexCharts registration
│   │
│   └── utils/
│       └── formatNumber.js           # Number abbreviation helper (1k, 1M, 1B)
│
└── public/                           # Publicly served static files
    ├── apple-touch-icon.png          # iOS home screen icon (180×180)
    ├── favicon-96x96.png             # PNG favicon (96×96)
    ├── favicon.ico                   # ICO favicon (multi-size)
    ├── favicon.svg                   # SVG favicon
    ├── robots.txt                    # Search engine crawl rules
    └── rtpoll-icon.svg               # Brand logo SVG
```

## 4. Environment & Configuration

### 4.1 Environment Variables

**File:** `.env.example`

| Variable | Description | Example |
|---|---|---|
| `API_URL` | Base URL for the REST API | `http://localhost:8000/api/v0` |
| `WS_URL` | Base URL for the WebSocket API | `ws://localhost:8000/api/v0/ws` |

These variables are exposed to the client via Nuxt's `runtimeConfig.public`, accessible as `apiBase` and `wsBase` respectively.

### 4.2 Nuxt Configuration

**File:** `nuxt.config.ts`

**Key decisions:**

| Setting | Value | Rationale |
|---|---|---|
| `ssr` | `true` | Global SSR enabled for SEO on marketing pages |
| `devtools` | `false` | Disabled in all environments |
| `devServer.host` | `0.0.0.0` | Allows access from Docker/network peers |
| `nitro.preset` | `cloudflare-pages` | Production deployment target |
| `vite.optimizeDeps.include` | ApexCharts packages | Pre-bundled for faster dev server cold starts |

## 5. Root Application Files

### 5.1 app.vue — Root Component

**File:** `app/app.vue`

The root component wraps all pages in `<NuxtLayout>` and `<NuxtPage>`, and sets global SEO metadata.

**Behavior:**
- Sets a dynamic `<title>` template: page titles render as `"Page Title | RTPoll"`
- Injects Open Graph and Twitter Card meta tags for social sharing
- Sets the `<html lang="en">` attribute for accessibility and SEO

### 5.2 error.vue — Global Error Page

**File:** `app/error.vue`

Handles Nuxt-level errors (404, 500, etc.) and renders within the `marketing` layout.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `error` | `Object` | Nuxt error object with `statusCode` and `message` |

**Behavior:**
- Displays the HTTP status code in a large heading using the Anton font
- Shows a contextual message: `"Page Not Found"` for 404, `"Something went wrong"` for others
- Includes a "Return Home" CTA button that navigates to `/`

## 6. Styling & Design System

**File:** `app/assets/css/global.css`

The global stylesheet establishes the entire visual identity of RTPoll through Tailwind CSS utilities and custom reusable classes.

### 6.1 Typography

**Fonts loaded:** [Google Fonts](https://fonts.google.com/) via `@import`:
- **Anton** — Used for headings (`h1`–`h4`), poll counters, and display text
- **Nunito** (weight 500, italic 500) — Primary body font

**Heading hierarchy:**

| Element | Font | Size | Color | Alignment |
|---|---|---|---|---|
| `h1` | Anton | `text-3xl` | `text-indigo-400` | Center |
| `h2` | Anton | `text-3xl` | `text-indigo-400` | Center |
| `h3` | Anton | `text-2xl` | `text-indigo-400` | Center |
| `h4` | Anton | `text-xl` | `text-indigo-400` | Center |
| `h5` | (Nunito) | `text-lg` | `text-indigo-400` | Center |

**Global HTML styles:**
```css
html {
    font-family: "Nunito", sans-serif;
    @apply text-indigo-900 break-words select-none box-border scroll-smooth;
}
```

### 6.2 Color Palette

The application uses Tailwind's **indigo** palette as the primary brand color:

| Role | Color | Tailwind Class |
|---|---|---|
| Primary | Indigo 400 | `text-indigo-400`, `bg-indigo-400` |
| Primary Hover | Indigo 500 | `hover:bg-indigo-500` |
| Primary Light | Indigo 100 | `bg-indigo-100` |
| Primary Surface | Indigo 50 | `bg-indigo-50` |
| Text Primary | Indigo 900 | `text-indigo-900` |
| Danger | Red 500 | `bg-red-500`, `text-red-500` |
| Danger Hover | Red 600 | `hover:bg-red-600` |
| Success | Green 500 | `text-green-500` |
| Neutral | Gray 400/500 | `text-gray-400`, `text-gray-500` |

### 6.3 Button System

Six button variants defined as global CSS classes:

| Class | Appearance | Use Case |
|---|---|---|
| `.btn` | Indigo filled, white text | Primary actions |
| `.btn-cancel` | White with gray border | Cancel / secondary actions |
| `.btn-alert` | Red filled, white text | Destructive actions |
| `.btn-disabled` | Indigo filled, 75% opacity, `cursor-wait` | Primary loading state |
| `.btn-cancel-disabled` | White bordered, 75% opacity | Cancel loading state |
| `.btn-alert-disabled` | Red filled, 75% opacity | Destructive loading state |

**All buttons share:** `py-2 px-4`, `rounded-md`, `font-medium`, `transition-all duration-500`, `active:scale-95`

**Interactive states:**
- **Hover:** Background darkens + `ring-4` glow effect with 30% opacity
- **Focus:** Background darkens
- **Active:** `scale-95` press animation
- **Disabled:** Reduced opacity, `cursor-wait`, no ring effects

### 6.4 Link System

| Class | Behavior |
|---|---|
| `.link` | Animated underline on hover (wavy decoration, `underline-offset-8`) |
| `.link-disabled` | `cursor-wait`, 75% opacity |
| `.link-icon` | Unstyled link with icon layout, indigo text, `hover:bg-indigo-100`, `active:scale-90` |

### 6.5 Form Elements

| Selector / Class | Styling |
|---|---|
| `label` | `font-medium`, `capitalize` |
| `input` | `outline-none` (base reset) |
| `.ipt`, `textarea`, `select` | Padded, bordered (`border-indigo-300`), rounded, focus ring in indigo |

### 6.6 Utility Classes

| Class | Purpose |
|---|---|
| `.no-style` | `all: unset` — complete style reset |
| `.error-msg` | Red 500 text, small size, centered |
| `.dashboard-body` | Full-width, padded flex container |
| `.bg-grid` | SVG-based subtle grid background pattern |
| `.notice` | Large Anton text, capitalised, supports line breaks |

## 7. Layouts

### 7.1 Default Layout

When no `layout` is specified in `definePageMeta()`, Nuxt uses the **default** layout. In this project, the default layout is not explicitly defined, so pages without a layout declaration render directly inside `<NuxtLayout>` from `app.vue` with no wrapping chrome.

### 7.2 marketing.vue

**File:** `app/layouts/marketing.vue`

The public-facing marketing layout wrapping the landing page, about page, and error page.

**Structure:**
```
┌─────────────────────────────────────┐
│        marketing/Navbar.vue         │  ← Sticky header with logo + auth links
├─────────────────────────────────────┤
│                                     │
│              <slot />               │  ← Page content
│                                     │
├─────────────────────────────────────┤
│        marketing/Footer.vue         │  ← Branded footer with navigation links
└─────────────────────────────────────┘
```

**CSS:** `min-h-screen flex flex-col` — ensures the footer always sits at the bottom.

### 7.3 dashboard.vue

**File:** `app/layouts/dashboard.vue`

The authenticated dashboard layout providing consistent navigation and notifications.

**Structure:**
```
┌─────────────────────────────────────┐
│          Header (sticky):           │
│  ┌─────────┐         ┌───────────┐  │
│  │ RTPoll  │         │ LogoutBtn │  │
│  │Dashboard│         │           │  │
│  └─────────┘         └───────────┘  │
├─────────────────────────────────────┤
│                                     │
│     PopupMessage (toast stack)      │  ← Fixed top-right
│                                     │
│          FloatingNavPanel           │  ← Fixed bottom center
│                                     │
│    ┌───────────────────────────┐    │
│    │         <slot />          │    │  ← Page content
│    └───────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- **Sticky header** (`sticky top-0 z-10`) with a white background, bottom border, and shadow
- The logo uses an **SVG text stroke outline** of "Dashboard" alongside the "RTPoll" name
- The header links to `/dashboard` and shows a logout button
- Main content has `pb-24` to prevent the floating nav from overlapping content
- `PopupMessage` renders the toast notification stack
- `FloatingNavPanel` provides quick access to Home, Create, and Settings

### 7.4 mail-redirect.vue

**File:** `app/layouts/mail-redirect.vue`

A minimal centered layout for email verification flows (verify-mail, update-mail, recover-pass).

**Structure:**
```
┌─────────────────────────────────────┐
│                                     │
│         ┌─────────────────┐         │
│         │    <slot />     │         │  ← Centered content (max-w-md)
│         └─────────────────┘         │
│                                     │
│           PoweredByFooter           │  ← "Powered by RTPoll" at bottom
└─────────────────────────────────────┘
```

**CSS:** `min-h-screen flex flex-col items-center justify-center px-4`

## 8. Middleware

All middleware runs **client-side only** (guarded with `import.meta.server` early returns) because auth state is stored in-memory and is not available during SSR.

### 8.1 auth.js

**File:** `app/middleware/auth.js`

**Purpose:** Protects authenticated routes. If the user is not logged in, it attempts a silent token refresh. If that fails, the user is redirected to the login page with the original URL preserved as a `redirect` query parameter.

**Flow:**
```
Request to protected route
    │
    ├─ Server-side? → Pass through (no-op)
    │
    ├─ isLoggedIn === true? → Allow access
    │
    └─ isLoggedIn === false
        └─ Try refresh()
            ├─ Success → Allow access
            └─ Failure → Redirect to /login?redirect=<originalPath>
```

**Applied to:** All `/dashboard/**` pages via `definePageMeta({ middleware: 'auth' })`.

### 8.2 guest.js

**File:** `app/middleware/guest.js`

**Purpose:** Prevents authenticated users from accessing login/register pages. If a user is already logged in, they are redirected to `/dashboard`.

**Flow:**
```
Request to guest-only route
    │
    ├─ Server-side? → Pass through (no-op)
    │
    ├─ isLoggedIn === true? → Redirect to /dashboard
    │
    └─ isLoggedIn === false
        └─ Try refresh() in background
            ├─ Success → Redirect to /dashboard
            └─ Failure → Allow access (stay on page)
```

**Applied to:** `/login`, `/register`, `/recover-pass`.

## 9. Composables

### 9.1 useApi

**File:** `app/composables/useApi.js`

A thin wrapper around Nuxt's `$fetch` that injects the API base URL and ensures credentials (cookies) are sent with every request.

**Returned interface:**

| Property | Type | Description |
|---|---|---|
| `api` | `Function(path, opts?)` | Executes `$fetch(apiBase + path, { credentials: "include", ...opts })` |
| `apiBase` | `String` | The configured API base URL from `runtimeConfig.public.apiBase` |

**Usage:**
```js
const { api } = useApi()
const data = await api('/auth/login', { method: 'POST', body: { email, password } })
```

### 9.2 useAuth

**File:** `app/composables/useAuth.js`  
**Lines:** 311

The core authentication composable managing the entire auth lifecycle. This is the most complex composable in the application.

**State:**

| Variable | Storage | Purpose |
|---|---|---|
| `accessToken` | `useState` (in-memory) | JWT access token — never stored in cookies/localStorage to prevent XSS |
| `timerState` | `useState` | Holds the `setTimeout` ID for scheduled token refresh |

**Returned interface:**

| Method / Property | Type | Description |
|---|---|---|
| `isLoggedIn` | `Computed<Boolean>` | `true` when an access token exists |
| `accessToken` | `Ref<String\|null>` | The current JWT access token |
| `login(email, password)` | `async Function` | Authenticates and stores the token |
| `register(email, password, confirm_password)` | `async Function` | Creates a new account |
| `logout()` | `async Function` | Invalidates the session server-side and clears local state |
| `refresh()` | `async Function → Boolean` | Refreshes the access token using the refresh token cookie |
| `authFetch(url, opts?)` | `async Function` | `$fetch` with `Authorization: Bearer <token>` header and automatic retry on 401 |
| `verifyEmail(token, newPassword?)` | `async Function` | Verifies email via token; optionally sets a new password |
| `resendVerification(email, type?)` | `async Function` | Resends the verification email |
| `sendPasswordResetEmail(email)` | `async Function` | Sends a password reset email |
| `changePassword(oldPassword, newPassword)` | `async Function` | Updates the user's password (requires auth) |
| `changeEmail(newEmail, password)` | `async Function` | Initiates email change (requires auth + password confirmation) |
| `deleteAccount(password)` | `async Function` | Permanently deletes the user's account (requires auth + password) |

**Key architectural decisions:**

1. **In-memory token storage:** The access token is held in a Vue `useState` ref — never persisted to `localStorage` or cookies — to prevent XSS-based token extraction.

2. **Cross-tab sync via `BroadcastChannel`:** A single `BroadcastChannel("auth_channel")` is created per browser session. It listens for three message types:
   - `LOGIN` — Propagates the new access token to all tabs
   - `REFRESH_SUCCESS` — Shares the refreshed token
   - `LOGOUT` — Clears auth state in all tabs

3. **Distributed refresh lock:** Uses `localStorage` keys (`auth_refresh_lock`, `auth_refresh_lock_time`) with a check-after-write pattern to ensure only **one tab** performs the refresh at a time. Stale locks (>10s) are automatically broken.

4. **Automatic token refresh:** When a token is obtained, `scheduleRefresh()` calculates `(expiresIn - 30s)` and sets a `setTimeout` to call `refresh()` before expiry. The delay is capped at 15 minutes to prevent issues with tampered tokens.

5. **401 retry in `authFetch`:** If a request returns 401, `authFetch` transparently calls `refresh()` and retries the original request with the new token.

6. **HMR cleanup:** The `BroadcastChannel` is closed during hot module replacement to prevent channel leaks in development.

### 9.3 usePopup

**File:** `app/composables/usePopup.js`

Manages a stack of toast notifications displayed via the `PopupMessage` component.

**State:**

| Variable | Storage | Purpose |
|---|---|---|
| `popups` | `useState("popups")` | Array of `{ id, message, type }` popup objects |

**Returned interface:**

| Method | Parameters | Description |
|---|---|---|
| `popups` | — | Reactive array of active popups |
| `showPopup(message, type?)` | `message: String`, `type: "success" \| "error"` | Adds a popup that auto-removes after 4 seconds |
| `showError(err, fallback?)` | `err: Error`, `fallback: String` | Extracts error messages from API responses and shows an error popup |
| `removePopup(id)` | `id: Number` | Manually removes a popup |

**Error extraction logic in `showError`:**
```
1. If err.data.detail is an Array → join all .msg values with ", "
2. Else if err.data.detail is a String → use it directly
3. Else → use the fallback message or "Something went wrong"
```

### 9.4 useValidation

**File:** `app/composables/useValidation.js`

Client-side form validation helpers that show error popups via `usePopup`.

**Returned interface:**

| Method | Parameters | Validation Rule | Error Message |
|---|---|---|---|
| `requireEmail(email, label?)` | `email: String` | Non-empty after `.trim()` | `"Please enter your {label} first."` |
| `requirePassword(password, label?)` | `password: String` | Non-empty (truthy) | `"Please enter your {label} first."` |
| `validatePasswordLength(password)` | `password: String` | `length >= 8` | `"Password must contain at least 8 characters."` |
| `validatePasswordMatch(password, confirmPassword)` | Two strings | Strict equality | `"Passwords do not match."` |

All methods return `true` if valid, `false` if invalid (and show the popup).

### 9.5 usePollToken

**File:** `app/composables/usePollToken.js`  
**Lines:** 273

Manages poll-scoped JWT tokens for both **creators** (authenticated via `authFetch`) and **visitors** (unauthenticated via `api`). These tokens authorize WebSocket connections.

**Constructor parameter:**

| Parameter | Type | Values | Description |
|---|---|---|---|
| `type` | `String` | `'visitor'` (default) or `'creator'` | Determines the API endpoint and fetch method |

**Token storage strategy:**
- **Primary:** `useCookie` (persisted across page refreshes, 3-day `maxAge`)
- **In-memory mirror:** `useState` (for reactive access within the application)

**Cookie names:**
- `visitor_poll_token` / `creator_poll_token` — The JWT itself
- `visitor_poll_token_expiry` / `creator_poll_token_expiry` — Token expiry timestamp

**Token endpoints:**
- **Visitor:** `POST /poll/visitor/token` (unauthenticated)
- **Creator:** `POST /poll/creator/token` (authenticated via `authFetch`)

**Returned interface:**

| Method / Property | Description |
|---|---|
| `token` | `Ref<String|null>` — Reactive poll token value |
| `generateToken()` | Fetches a new token from the server |
| `ensureToken()` | Returns a valid token; refreshes if expired |
| `clearToken()` | Clears all token state, cookies, and timers |
| `isExpired()` | Returns `true` if the token is expired |

**Cross-tab synchronization:**
- Uses a `BroadcastChannel` (`visitor_poll_token_channel` or `creator_poll_token_channel`) to propagate refreshed tokens
- Uses a `localStorage` lock (identical pattern to `useAuth`) to prevent concurrent refresh races
- Listens for `storage` events as a fallback for cross-tab token propagation

**Auto-refresh:** Scheduled 60 seconds before token expiry. Maximum delay capped at 24 hours.

### 9.6 useWebSocket

**File:** `app/composables/useWebSocket.js`  
**Lines:** 102

A reusable WebSocket connection manager with automatic reconnection and exponential backoff.

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `urlRef` | `Ref<String> \| Function` | Reactive URL or a function returning the WebSocket URL |
| `options` | `Object` | Configuration options (see below) |

**Options:**

| Option | Type | Default | Description |
|---|---|---|---|
| `onMessage` | `Function(data)` | `() => {}` | Callback for incoming messages (auto-parsed from JSON) |
| `onError` | `Function()` | `() => {}` | Callback for connection errors |
| `maxRetries` | `Number` | `10` | Maximum reconnection attempts |
| `baseDelay` | `Number (ms)` | `1000` | Initial reconnection delay |
| `maxDelay` | `Number (ms)` | `16000` | Maximum reconnection delay cap |

**Returned interface:**

| Property / Method | Type | Description |
|---|---|---|
| `status` | `Ref<String>` | `'closed'`, `'connecting'`, `'open'`, or `'error'` |
| `connect()` | `Function` | Opens a WebSocket connection |
| `send(data)` | `Function → Boolean` | Sends data (auto-serialized to JSON); returns `false` if socket is not open |
| `close()` | `Function` | Intentionally closes the connection (no reconnection) |

**Reconnection strategy:**
```
Delay = min(baseDelay × 2^retryCount, maxDelay)

Retry 0: 1000ms
Retry 1: 2000ms
Retry 2: 4000ms
Retry 3: 8000ms
Retry 4+: 16000ms (capped)
```

**Lifecycle:** Automatically closes on `onBeforeUnmount` to prevent memory leaks.

## 10. Plugins

### 10.1 apexcharts.client.js

**File:** `app/plugins/apexcharts.client.js`

Registers the `vue3-apexcharts` component globally as a Vue plugin. The `.client.js` suffix ensures this plugin runs **only on the client side** (not during SSR), since ApexCharts requires browser APIs.

After registration, the `<apexchart>` component is available globally without imports. It is wrapped in `<ClientOnly>` in templates to prevent SSR hydration mismatches.

## 11. Utilities

### 11.1 formatNumber

**File:** `app/utils/formatNumber.js`

Converts large numbers into human-readable abbreviated strings. Nuxt auto-imports this utility throughout the application.

| Input Range | Output |
|---|---|
| `≥ 1,000,000,000` | `{n}B` (e.g., `1.5B`) |
| `≥ 1,000,000` | `{n}M` (e.g., `2.3M`) |
| `≥ 1,000` | `{n}k` (e.g., `10k`) |
| `< 1,000` | Raw number as string |

Trailing `.0` is stripped (e.g., `1.0k` → `1k`).

**Used by:** `PollCard.vue`, `poll/[id].vue` — to display vote counts.

## 12. Pages (Routing)

### 12.1 Route Map

| Route | Page File | Layout | Middleware | SSR | Description |
|---|---|---|---|---|---|
| `/` | `pages/index.vue` | `marketing` | — | &check; | Landing page |
| `/about` | `pages/about.vue` | `marketing` | — | &check; | About us / team |
| `/login` | `pages/login.vue` | (none) | `guest` | &cross; | Login form |
| `/register` | `pages/register.vue` | (none) | `guest` | &cross; | Registration form |
| `/recover-pass` | `pages/recover-pass.vue` | `mail-redirect` | `guest` | &cross; | Password reset (email link target) |
| `/verify-mail` | `pages/verify-mail.vue` | `mail-redirect` | — | &cross; | Email verification (email link target) |
| `/update-mail` | `pages/update-mail.vue` | `mail-redirect` | — | &cross; | Email change confirmation |
| `/contact` | `pages/contact.vue` | (none) | — | — | Contact form (currently empty) |
| `/privacy-policy` | `pages/privacy-policy.vue` | (none) | — | — | Privacy Policy (currently empty) |
| `/poll/:id` | `pages/poll/[id].vue` | (none) | — | &cross; | Public poll voting page |
| `/dashboard` | `pages/dashboard/index.vue` | `dashboard` | `auth` | &cross; | Poll list (running + closed tabs) |
| `/dashboard/create` | `pages/dashboard/create.vue` | `dashboard` | `auth` | &cross; | Create new poll form |
| `/dashboard/settings` | `pages/dashboard/settings.vue` | `dashboard` | `auth` | &cross; | User settings |
| `/dashboard/poll/:id` | `pages/dashboard/poll/[id].vue` | `dashboard` | `auth` | &cross; | Poll detail view (creator) |

### 12.2 Public Pages

#### `pages/index.vue` — Landing Page

**Layout:** `marketing`  
**Title:** (empty — renders as just "RTPoll" due to title template)

**Sections:**

1. **Hero Section** — Headline (`"Make Your Own Polling and Share Easily with RTPoll"`), description text, vertically centered.

2. **Wave Transition** — An inline SVG with 7 layered wave paths (opacity gradient from 0.05 to 1.0) creating a smooth visual transition from white to the indigo features section.

3. **Features Section** — A 2×2 responsive grid (`grid-cols-1 md:grid-cols-2`) with 4 feature cards:
   - **Create Polls** — Multi-option poll creation
   - **Share Polls** — Public links, anonymous voting
   - **Real-time Results** — Live vote updates
   - **Visual Analysis** — Last 30-day vote trend graphs

   Each card has:
   - An SVG icon in an indigo pill that inverts colors on hover
   - A heading and description
   - Hover effects: shadow intensification, slight upward translation (`hover:-translate-y-2`)

4. **Call-to-Action Section** — Gradient fade from indigo to transparent, followed by a "Create Polls in a Minute" heading and a "Get Started" button linking to `/register`.

#### `pages/about.vue` — About Page

**Layout:** `marketing`  
**Title:** `"About Us"`

**Sections:**

1. **About Section** — Large heading, descriptive paragraph, and three pill badges:
   - Real-time Updates
   - Secure Voting
   - Live Analytics

   Each badge uses an Iconify icon from the `fluent` icon set.

2. **Team Section** — Two `ProfileCard` components displaying team members:
   - **Atia Farha** (Frontend Developer) — GitHub + LinkedIn links
   - **S.M Nazmus Sadat** (Backend Developer) — GitHub + LinkedIn links

### 12.3 Authentication Pages

#### `pages/login.vue` — Login Page

**Middleware:** `guest`  
**Title:** `"Login"`

**Features:**
- Email and password inputs with client-side validation via `useValidation`
- "Forgot password?" link opens `ForgotPasswordWindow` modal
- On successful login, redirects to `route.query.redirect` or `/dashboard`
- If the server returns HTTP `428` (email not verified), shows a "Resend verification email" link
- Cross-links to `/register`
- Uses `bg-grid` background pattern
- The form card has a glassmorphism effect (`backdrop-blur-[100px]`, border, shadow)

#### `pages/register.vue` — Registration Page

**Middleware:** `guest`  
**Title:** `"Register"`

**Features:**
- Email, password, and confirm password inputs
- Full validation chain: `requireEmail` → `requirePassword` → `validatePasswordLength` → `validatePasswordMatch`
- On success, shows a success popup and redirects to `/login`
- Cross-links to `/login`
- Same visual treatment as the login page

### 12.4 Email Action Pages

All three share the `mail-redirect` layout and read a token from the `?t=` query parameter.

#### `pages/verify-mail.vue` — Email Verification

**SSR:** Disabled  
**Flow:**
1. On mount, reads `route.query.t`
2. If no token → shows error
3. Calls `verifyEmail(token)` via `useAuth`
4. On success → shows success message, auto-redirects to `/login` after 2 seconds
5. On error → shows error with link to login

#### `pages/update-mail.vue` — Email Change Confirmation

Identical flow to `verify-mail.vue`. Confirms the user's email change by verifying the token sent to their new address.

#### `pages/recover-pass.vue` — Password Reset

**Middleware:** `guest`  
**SSR:** Disabled

**Flow:**
1. On mount, checks for `route.query.t`
2. If no token → shows error
3. Presents a password input form
4. Calls `verifyEmail(token, newPassword)` to set the new password
5. On `406` error → shows password length validation message
6. On success → shows success popup, auto-redirects to `/login` after 2 seconds

### 12.5 Dashboard Pages (Authenticated)

All dashboard pages use the `dashboard` layout and `auth` middleware.

#### `pages/dashboard/index.vue` — Dashboard Home

**Title:** `"Dashboard"`

**Features:**
- **Tab toggle** between "Running Polls" and "Closed Polls" using a segmented pill button (left rounded, right rounded)
- Conditionally renders `<RunningPollView>` or `<ClosedPollView>` based on `activeTab` ref

#### `pages/dashboard/create.vue` — Create Poll

**Title:** `"Create Poll"`

**Form fields:**

| Field | Type | Default | Validation |
|---|---|---|---|
| Duration | `<select>` | `"infinite"` | If `"custom"`, shows datetime-local picker |
| Custom Duration | `<input type="datetime-local">` | — | Min = current time |
| Show Results Publicly | `<select>` | `"no"` | `"yes"` or `"no"` |
| Question | `<textarea>` | — | Required, max 1024 chars |
| Options | Dynamic `<input>` list | 2 empty inputs | Min 2, max 10, each max 256 chars, no blanks |

**Behaviors:**
- "Add Option" button (capped at 10 with popup warning)
- Each option has a "✕" remove button (disabled when only 2 remain)
- On submit, sends `POST /poll` via `authFetch` with `{ question, options, expires_at, result_public }`
- On success, navigates to `/dashboard/poll/{poll_id}`

#### `pages/dashboard/settings.vue` — User Settings

**Title:** `"Settings"`

**Sections:**

1. **Account Info**
   - `ChangeEmail` component — Pre-filled with current email
   - Account creation date (formatted as `"Month Day, Year"`)
   - Stats grid: Total Polls, Running Polls, Closed Polls

2. **Change Password**
   - `ChangePassword` component

3. **Danger Zone** (red-themed)
   - `DeleteClosedPollBtn` — Deletes all expired polls
   - `DeleteAllPollBtn` — Deletes all polls
   - `DeleteAccountBtn` — Permanently deletes the account

**Data fetching:** On mount, fetches `GET /user` via `authFetch` to populate the user profile data.

#### `pages/dashboard/poll/[id].vue` — Poll Detail (Creator View)

**Title:** `"Poll Details"`

**Features:**

1. **Share bar** — Read-only URL input with a share button (uses `navigator.share` with clipboard fallback)
2. **Poll settings** — `PollSettings` dropdown with delete action
3. **Question card** — Indigo header with white text, option list with vote percentages
4. **Countdown timer** — `vue3-flip-countdown` with indigo theme (shown only for non-infinite, non-expired polls)
5. **Expired notice** — Gray bordered message when poll has expired
6. **Metadata grid** — 2×2 grid showing Creation Time, Expiry Time, Total Votes, Results visibility
7. **Votes table** — Simple two-column table (Option No. / Votes Received)
8. **Graph view** — `GraphView` component with last 30-day vote history chart

**Real-time updates:**
- Acquires a `creator` poll token via `usePollToken('creator')`
- Connects to `{wsBase}/{poll_id}?t={token}` via `useWebSocket`
- On `results` messages: updates `total_votes`, `option_perc[]`, and `option_votes[]` reactively

### 12.6 Public Poll Voter Page

#### `pages/poll/[id].vue` — Public Voting Page

**Title:** `"Vote in Poll"`  
**Layout:** None (standalone with `PoweredByFooter`)

**Features:**

1. **Countdown timer** — Flip countdown for polls with expiry dates
2. **Question card** — Indigo header with radio button options
3. **Vote count** — Total votes displayed with fire icon and abbreviated number
4. **Voting** — Clicking a radio button sends a WebSocket message `{ type: "update", option_id }` instantly

**Anti-fraud:**
- Uses **FingerprintJS** to generate a `visitorId` browser fingerprint
- The fingerprint is passed as a `fp` query parameter on the WebSocket URL

**Real-time updates:**
- Acquires a `visitor` poll token via `usePollToken('visitor')`
- Connects to `{wsBase}/{poll_id}?t={token}&fp={fingerprint}`
- On `results` messages: updates `total_votes` and `option_perc[]`
- On `notice` messages: displays notice text (e.g., poll expired)
- On `error` messages: shows error popup

**State handling:**
- `loading` → Shows `<Loading>` spinner
- `error` → Shows error in a red double-border box
- `notice` → Shows notice in an indigo double-border box
- Normal → Shows the voting UI

### 12.7 Placeholder Pages

| Page | Content |
|---|---|
| `pages/contact.vue` | Empty template (`<template></template>`) |
| `pages/privacy-policy.vue` | Empty template (`<template></template>`) |

## 13. Components

### 13.1 Component Hierarchy

```
app.vue
├── NuxtLayout
│   ├── marketing.vue
│   │   ├── marketing/Navbar.vue
│   │   └── marketing/Footer.vue
│   │
│   ├── dashboard.vue
│   │   ├── LogoutBtn.vue
│   │   ├── PopupMessage.vue
│   │   └── FloatingNavPanel.vue
│   │
│   └── mail-redirect.vue
│       └── PoweredByFooter.vue
│
├── Pages
│   ├── index.vue (landing)
│   ├── about.vue
│   │   └── ProfileCard.vue
│   ├── login.vue
│   │   ├── PopupMessage.vue
│   │   └── ForgotPasswordWindow.vue
│   ├── register.vue
│   │   └── PopupMessage.vue
│   ├── dashboard/index.vue
│   │   ├── RunningPollView.vue
│   │   │   ├── Loading.vue
│   │   │   └── PollCard.vue
│   │   └── ClosedPollView.vue
│   │       ├── Loading.vue
│   │       └── PollCard.vue
│   ├── dashboard/create.vue
│   ├── dashboard/settings.vue
│   │   ├── ChangeEmail.vue
│   │   ├── ChangePassword.vue
│   │   ├── DeleteClosedPollBtn.vue
│   │   ├── DeleteAllPollBtn.vue
│   │   └── DeleteAccountBtn.vue
│   ├── dashboard/poll/[id].vue
│   │   ├── PollSettings.vue
│   │   └── GraphView.vue
│   └── poll/[id].vue
│       ├── PopupMessage.vue
│       └── PoweredByFooter.vue
│
└── error.vue
```

### 13.2 Marketing Components

#### `marketing/Navbar.vue`

**Purpose:** Responsive navigation bar for public marketing pages.

| State | Type | Description |
|---|---|---|
| `menu` | `ref(false)` | Mobile hamburger menu toggle |

**Structure:**
- **Left:** Logo (SVG icon + SVG outlined text "RTPoll") linking to `/`
- **Right:** Login and Sign Up buttons
- **Mobile:** Hamburger menu (three horizontal spans), toggles navigation visibility
- Login button: outlined style; Sign Up button: filled style
- Breakpoint: `sm:` (640px) switches from vertical mobile to horizontal desktop layout

#### `marketing/Footer.vue`

**Purpose:** Full-width branded footer with navigation links organized in three columns.

**Link groups:**

| Column | Label | Links |
|---|---|---|
| Platform | `Features`, `About Us` | `/#features`, `/about` |
| Account | `Login`, `Sign Up` | `/login`, `/register` |
| Support | `Contact Us`, `Privacy Policy` | `#` (placeholder), `#` (placeholder) |

**Visual:** Indigo 400 background, white text, "RTPoll" in large Anton font, responsive column layout.

### 13.3 Dashboard Navigation Components

#### `FloatingNavPanel.vue`

**Purpose:** Fixed bottom navigation dock providing quick access to the three main dashboard sections.

**Icons (Iconify):**
| Icon | Destination | Title |
|---|---|---|
| `ion:file-tray-outline` | `/dashboard` | Home |
| `system-uicons:create` | `/dashboard/create` | Create Poll |
| `solar:settings-outline` | `/dashboard/settings` | Settings |

**Visual:** Fixed to `bottom-6`, centered (`left-1/2 -translate-x-1/2`), white background with indigo border, rounded, shadow. The "Create" button is a prominent circular indigo FAB (Floating Action Button) elevated above the bar using absolute positioning.

#### `LogoutBtn.vue`

**Purpose:** Icon-only logout button displayed in the dashboard header.

**Behavior:**
1. Sets `loading` state
2. Calls `logout()` from `useAuth`
3. Navigates to `/login`
4. On error: shows popup via `showError`

**Icon:** `carbon:logout` (Iconify)

### 13.4 Notification Components

#### `PopupMessage.vue`

**Purpose:** Renders a stack of toast notifications in the top-right corner of the viewport.

**Position:** `fixed top-10 right-6 z-50`

**Popup rendering:**
- Each popup has a width of 280px with colored border, background, and text
- **Success:** Green theme (`bg-green-50 text-green-500 border-green-500`)
- **Error:** Red theme (`bg-red-50 text-red-500 border-red-500`)
- Each popup has a close `×` button

**Animations (scoped CSS):**
- **Enter:** Fades in with right-to-left slide (`translateX(40px)` → `translateX(0)`)
- **Leave:** Fades out with left-to-right slide
- **Move:** Smooth repositioning when items are added/removed

Uses Vue's `<TransitionGroup>` with `name="toast"`.

### 13.5 Poll Display Components

#### `PollCard.vue`

**Purpose:** Reusable card displaying a poll summary. Used in both `RunningPollView` and `ClosedPollView`.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `question` | `String` | Poll question text (line-clamped to 2 lines) |
| `top_option` | `String` | Name of the leading option (truncated) |
| `total_votes` | `Number` | Total vote count (formatted via `formatNumber`) |
| `expires_at` | `String` | Expiry date string |

**Icons:** `pajamas:expire` (clock), `lets-icons:fire-fill` (fire)

**Visual:** 400px max width, 180px height, indigo gradient hover effect, press animation (`active:scale-90`).

#### `RunningPollView.vue`

**Purpose:** Fetches and displays paginated active (non-expired) polls.

**API call:** `GET /poll?expired=false&page={n}` via `authFetch`

**Pagination system:**
- Tracks `running_page`, `running_pages`
- Shows a windowed page range (current ± 2 pages) with ellipsis
- Previous/Next arrow buttons (`&#10229;` / `&#10230;`)
- Active page: indigo filled; inactive: gray bordered

**States:** Loading spinner, error message, empty state `"( No running poll )"`, or poll grid.

**Each poll** is rendered as a `PollCard` component. Clicking navigates to `/dashboard/poll/{id}`.

#### `ClosedPollView.vue`

**Purpose:** Identical structure to `RunningPollView` but fetches expired polls.

**API call:** `GET /poll?expired=true&page={n}` via `authFetch`

Same pagination system, same states, same card layout.

#### `GraphView.vue`

**Purpose:** Displays a last 30-day vote history bar chart using ApexCharts.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `poll_id` | `String` | The poll ID to fetch history for |

**API call:** `GET /poll/{poll_id}/history` via `authFetch`

**Chart configuration:**
```js
{
    chart: { type: "bar", toolbar: { show: true } },
    colors: ['#818CF8'],            // Indigo 400
    stroke: { curve: "smooth" },
    xaxis: { type: "datetime", labels: { format: "dd MMM yyyy" } },
    tooltip: { x: { format: "dd-mm-yyyy" } }
}
```

**Features:**
- Manual refresh button with spinning icon animation
- Error state display
- Empty state: `"( No graph data )"`
- Note about data being available for up to last 30 days
- Wrapped in `<ClientOnly>` to prevent SSR issues

#### `PollSettings.vue`

**Purpose:** Gear icon with a dropdown menu for poll management actions.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `poll_id` | `String` | The poll to manage |

**Behavior:**
1. Click gear icon → shows dropdown with "Delete" button
2. Click "Delete" → opens confirmation modal
3. Confirm → calls `DELETE /poll/{poll_id}` via `authFetch`
4. Success → navigates to `/dashboard`

**Click-outside handling:** Adds/removes a `click` event listener on `document` in `onMounted` / `onUnmounted` to close the dropdown when clicking outside.

### 13.6 Settings Components

#### `ChangeEmail.vue`

**Props:**
| Prop | Type | Description |
|---|---|---|
| `email` | `String` | Current email (pre-fills the input) |

**Flow:**
1. User edits the email input and clicks "Change Email"
2. Confirmation modal opens explaining that a verification email will be sent
3. User enters password in the modal
4. Client validates: `requireEmail`, `requirePassword`, `validatePasswordLength`
5. Calls `changeEmail(newEmail, password)` from `useAuth`
6. Success → shows popup, closes modal

**Reactive sync:** Watches `props.email` and syncs to local `email` ref with `{ immediate: true }`.

#### `ChangePassword.vue`

**Flow:**
1. Collects current password, new password, and confirm password
2. Validates all three with `requirePassword`, `validatePasswordLength`, and `validatePasswordMatch`
3. Calls `changePassword(oldPassword, newPassword)` from `useAuth`
4. Success → shows popup

#### `DeleteAccountBtn.vue`

**Flow:**
1. Click "Delete Account" → opens confirmation modal with red-themed heading
2. User enters password
3. Validates password
4. Calls `deleteAccount(password)` from `useAuth`
5. Calls `logout()` and navigates to `/login`
6. Modal includes a warning: *"All your polls and data will be lost. This action cannot be undone."*

**Input styling:** Uses red-themed border and focus ring (different from the standard `.ipt` class).

#### `DeleteAllPollBtn.vue`

**Flow:**
1. Click "Delete All Polls" → confirmation modal
2. Confirm → `DELETE /poll` via `authFetch`
3. Success → popup, modal closes

**Button style:** Red outlined (`border-2 border-red-500 text-red-500`).

#### `DeleteClosedPollBtn.vue`

**Flow:**
1. Click "Delete All Closed Polls" → confirmation modal
2. Confirm → `DELETE /poll?expired=true` via `authFetch`
3. Success → popup, modal closes

### 13.7 Shared UI Components

#### `Loading.vue`

**Purpose:** Centered animated loading spinner.

**Icon:** `eos-icons:bubble-loading` (Iconify) — animated bubble dots in indigo.

#### `PoweredByFooter.vue`

**Purpose:** Minimal footer displaying "Powered by RTPoll" with a link to the home page.

**Used by:** `mail-redirect.vue` layout, `poll/[id].vue` page.

#### `ProfileCard.vue`

**Purpose:** Team member profile card used on the About page.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `name` | `String` | Team member's name |
| `role` | `String` | Role title |
| `github` | `String` | GitHub profile URL |
| `linkedin` | `String` | LinkedIn profile URL |

**Visual:** 19em wide card with indigo border, name/role section, and a bottom bar split between GitHub and LinkedIn icon buttons.

#### `ForgotPasswordWindow.vue`

**Purpose:** Modal dialog for requesting a password reset email.

**Props:**
| Prop | Type | Description |
|---|---|---|
| `open` | `Boolean` | Controls modal visibility |

**Emits:** `close`

**Flow:**
1. User enters email address
2. Validates with `requireEmail`
3. Calls `sendPasswordResetEmail(email)` from `useAuth`
4. Success → popup, closes modal

**Dismissal:** Click on backdrop (`.self` modifier) or complete the flow.

## 14. State Management

RTPoll uses **Nuxt's built-in `useState`** for global reactive state instead of Pinia or Vuex. State is managed entirely through composables:

| State Key | Composable | Purpose |
|---|---|---|
| `auth_access_token` | `useAuth` | JWT access token |
| `auth_refresh_timer` | `useAuth` | Refresh timer ID |
| `popups` | `usePopup` | Active toast notifications |
| `visitorPollToken` | `usePollToken('visitor')` | Visitor poll JWT |
| `visitorPollTokenExpiry` | `usePollToken('visitor')` | Visitor token expiry |
| `visitorPollTokenRefreshTimer` | `usePollToken('visitor')` | Visitor token refresh timer |
| `creatorPollToken` | `usePollToken('creator')` | Creator poll JWT |
| `creatorPollTokenExpiry` | `usePollToken('creator')` | Creator token expiry |
| `creatorPollTokenRefreshTimer` | `usePollToken('creator')` | Creator token refresh timer |

## 15. Authentication Architecture

### 15.1 Token Strategy

The application implements a **dual-token strategy**:

| Token | Storage | Lifetime | Sent Via |
|---|---|---|---|
| **Access Token** (JWT) | In-memory (`useState`) | Short-lived (server-configured) | `Authorization: Bearer <token>` header |
| **Refresh Token** | HTTP-only cookie (set by backend) | Long-lived | Automatically via `credentials: "include"` |

**Security rationale:**
- The access token is **never** stored in `localStorage`, `sessionStorage`, or non-HttpOnly cookies — preventing XSS-based token theft.
- The refresh token cookie is set by the backend with `HttpOnly`, `Secure`, and `SameSite` flags, making it inaccessible to JavaScript.

### 15.2 Cross-Tab Synchronization

```
Tab A                  BroadcastChannel            Tab B
  │                     "auth_channel"                │
  │                                                   │
  ├─ login() ──────────────── LOGIN ────────────────► │
  │                       {accessToken}               │
  │                                                   ├─ Updates token
  │                                                   ├─ Schedules refresh
  │                                                   │
  ├─ refresh() ────────── REFRESH_SUCCESS ──────────► │
  │  (lock holder)         {accessToken}              │
  │                                                   ├─ Updates token
  │                                                   │
  ├─ logout() ─────────────── LOGOUT ───────────────► │
  │                                                   ├─ Clears auth state
```

### 15.3 Auto-Refresh Mechanism

```
Token obtained
    │
    ├─ Parse JWT payload → extract `exp` claim
    │
    ├─ Calculate: delay = max((exp - now - 30s) × 1000, 5000)
    │
    ├─ Cap: delay = min(delay, 15 minutes)
    │
    └─ setTimeout(refresh, delay)
           │
           └─ Acquire localStorage lock
               |
               ├─ Got lock? → Call POST /auth/refresh
               │                ├─ Success → Update token, broadcast, reschedule
               │                └─ Failure → Clear auth, broadcast LOGOUT
               |
               └─ No lock? → Wait for BroadcastChannel message (5s timeout fallback)
```

### 15.4 Auth Flow Diagrams

**Login Flow:**
```
User submits credentials
    → POST /auth/login { email, password }
    → Server returns { access_token } + sets refresh cookie
    → Store access_token in useState
    → Schedule auto-refresh
    → Broadcast LOGIN to other tabs
    → Navigate to redirect URL or /dashboard
```

**401 Retry Flow (authFetch):**
```
authFetch(url, opts)
    → Send request with Authorization header
    → 401 response?
        → refresh()
            → Success? → Retry request with new token
            → Failure? → Throw original error
    → Other error? → Throw error
```

## 16. Real-Time Architecture (WebSocket)

### 16.1 Connection Flow

```
Page Mount (poll/[id].vue or dashboard/poll/[id].vue)
    │
    ├─ ensureToken() — Obtain valid poll token (visitor or creator)
    │
    ├─ fetchPollDetails() — Load initial poll data via REST API
    │
    ├─ [Voter only] getVisitorId() — Generate browser fingerprint via FingerprintJS
    │
    └─ connectWS() — Open WebSocket connection
         URL: {wsBase}/{poll_id}?t={token}[&fp={fingerprint}]
```

### 16.2 Poll Token System

Two distinct token types authorize WebSocket access:

| Type | Endpoint | Auth Required | Cookie Name | Purpose |
|---|---|---|---|---|
| `visitor` | `POST /poll/visitor/token` | No | `visitor_poll_token` | Authorizes anonymous voters |
| `creator` | `POST /poll/creator/token` | Yes (Bearer) | `creator_poll_token` | Authorizes poll owners to view full results |

Both types use identical cross-tab synchronization and auto-refresh logic (see `usePollToken`).

### 16.3 Message Protocol

**Incoming messages (server → client):**

| `type` | Fields | Description | Handler |
|---|---|---|---|
| `results` | `total_votes`, `option_perc[]`, `option_votes[]` (creator only) | Updated vote tallies | Updates `poll.value` reactively |
| `error` | `detail` | Server-side error | Shows error popup (voter) or silent (creator) |
| `notice` | `detail` | Poll status change | Sets `notice` text (voter only) |

**Outgoing messages (client → server):**

| `type` | Fields | Description | Sender |
|---|---|---|---|
| `update` | `option_id` | Cast a vote | Voter page only |

### 16.4 Reconnection Strategy

Handled by `useWebSocket` with exponential backoff:

| Attempt | Delay |
|---|---|
| 1 | 1s |
| 2 | 2s |
| 3 | 4s |
| 4 | 8s |
| 5–10 | 16s (capped) |
| >10 | No further retries |

Reconnection is suppressed if `close()` was called intentionally. The connection is automatically cleaned up on component unmount.

## 17. API Integration

### 17.1 Endpoint Map

All endpoints are prefixed with the value of `API_URL` (e.g., `/api/v0`).

**Authentication:**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/login` | No | Login, returns access token + sets refresh cookie |
| `POST` | `/auth/register` | No | Register new account |
| `POST` | `/auth/refresh` | Cookie | Refresh access token |
| `POST` | `/auth/logout` | Cookie | Invalidate session |
| `POST` | `/auth/email/verify` | No | Verify email (with optional new password) |
| `POST` | `/auth/email/resend` | No | Resend verification email |

**User Management:**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/user` | Bearer | Fetch user profile (email, stats) |
| `PATCH` | `/user` | No | Send password reset email |
| `PUT` | `/user` | Bearer | Change password |
| `POST` | `/user` | Bearer | Request email change |
| `DELETE` | `/user` | Bearer | Delete account |

**Poll Management (Authenticated):**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/poll?expired={bool}&page={n}` | Bearer | List user's polls (paginated) |
| `POST` | `/poll` | Bearer | Create new poll |
| `GET` | `/poll/{id}` | Bearer | Get poll details (creator view) |
| `DELETE` | `/poll/{id}` | Bearer | Delete a specific poll |
| `DELETE` | `/poll` | Bearer | Delete all polls |
| `DELETE` | `/poll?expired=true` | Bearer | Delete all closed polls |
| `GET` | `/poll/{id}/history` | Bearer | Get last 30-day vote history |

**Poll Tokens:**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/poll/visitor/token` | No | Generate visitor WebSocket token |
| `POST` | `/poll/creator/token` | Bearer | Generate creator WebSocket token |

**Public Voter:**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/voter/{poll_id}` | No | Get poll data for public voting page |

**WebSocket:**

| URL | Auth | Description |
|---|---|---|
| `{WS_URL}/{poll_id}?t={token}&fp={fingerprint}` | Token | Voter real-time connection |
| `{WS_URL}/{poll_id}?t={token}` | Token | Creator real-time connection |

### 17.2 Error Handling

The application uses a standardized error extraction pattern across all pages and components:

```js
// Pattern used in catch blocks:
const message = Array.isArray(err?.data?.detail)
    ? err.data.detail.map((e) => e.msg).join(", ")
    : err?.data?.detail || fallbackMessage
```

This handles three backend response formats:
1. **Validation errors** (FastAPI/Pydantic): `{ detail: [{ msg: "..." }, ...] }`
2. **String errors:** `{ detail: "Error message" }`
3. **Unknown errors:** Falls back to a hardcoded message

## 18. SEO & Meta Configuration

| Feature | Implementation |
|---|---|
| **Title Template** | `"{Page Title} \| RTPoll"` or `"RTPoll"` for the home page |
| **Meta Description** | Set globally in `app.vue` |
| **Open Graph** | `og:title`, `og:description`, `og:type`, `og:site_name` |
| **Twitter Cards** | `twitter:title`, `twitter:description`, `twitter:card` (summary_large_image) |
| **HTML Language** | `<html lang="en">` |
| **robots.txt** | `User-Agent: *` / `Disallow:` (allows all crawlers) |
| **Per-page titles** | Set via `useHead({ title: '...' })` in each page |

**SSR-rendered pages** (`/`, `/about`) benefit from full server-rendered HTML for search engine indexing.

## 19. Static Assets

**Directory:** `public/`

| File | Purpose |
|---|---|
| `favicon.ico` | Multi-size ICO favicon |
| `favicon.svg` | SVG favicon (modern browsers) |
| `favicon-96x96.png` | PNG favicon (96×96) |
| `apple-touch-icon.png` | iOS home screen icon |
| `rtpoll-icon.svg` | Brand logo SVG (used in Navbar) |
| `robots.txt` | Search engine crawl rules |

## 20. Build & Deployment

### 20.1 Scripts

| Script | Command | Description |
|---|---|---|
| `dev` | `nuxt dev` | Starts the dev server (host `0.0.0.0`) |
| `build` | `nuxt build` | Builds for production |
| `generate` | `nuxt generate` | Pre-renders static pages |
| `preview` | `nuxt preview` | Previews the production build locally |
| `postinstall` | `nuxt prepare` | Generates TypeScript types after installing dependencies |

### 20.2 SSR Strategy

The application uses a **hybrid rendering** approach configured via `routeRules`:

| Route Pattern | Rendering | Rationale |
|---|---|---|
| `/` | SSR | SEO — landing page needs server-rendered HTML |
| `/about` | SSR | SEO — static content |
| `/login` | CSR only | Auth state is client-side only |
| `/register` | CSR only | Auth state is client-side only |
| `/recover-pass` | CSR only | Reads query params client-side |
| `/verify-mail` | CSR only | Reads query params client-side |
| `/update-mail` | CSR only | Reads query params client-side |
| `/dashboard/**` | CSR only | Authenticated content, no SEO needed |
| `/poll/**` | CSR only | Dynamic content with WebSocket |

### 20.3 Deployment Target

**Platform:** [Cloudflare Pages](https://pages.cloudflare.com/)

```ts
// nuxt.config.ts
nitro: {
    preset: 'cloudflare-pages',
    cloudflare: { nodeCompat: true }
}
```

The `nodeCompat: true` flag enables Node.js compatibility mode in Cloudflare Workers, allowing Node.js-specific APIs.

## 21. Development Guide

### Prerequisites

- **Node.js** (compatible with Nuxt 4)
- **pnpm** (package manager)

### Setup

```bash
cd frontend
pnpm install
pnpm approve-builds
```

### Local Development

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Start the dev server:
   ```bash
   pnpm dev
   ```
   The app will be available at [http://http://127.0.0.1:3000](http://127.0.0.1:3000/) in the browser of your device.

### Production Build

```bash
pnpm build
pnpm preview    # Preview the build locally
```

### Git Ignore Rules

The following paths are ignored in version control:

| Path | Reason |
|---|---|
| `.output`, `.data`, `.nuxt`, `.nitro`, `.cache`, `dist` | Nuxt build artifacts |
| `node_modules` | Dependencies |
| `logs`, `*.log` | Log files |
| `.DS_Store`, `.fleet`, `.idea` | IDE/OS files |
| `.env`, `.env.*` (except `.env.example`) | Sensitive environment variables |