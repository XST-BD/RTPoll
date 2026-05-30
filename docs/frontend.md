# RTPoll - Frontend Documentation

This is the documentation for the frontend of RTPoll project.

## Frontend Technologies

- **[Nuxt.js](https://nuxt.com/)** - Vue.js framework
- **[Tailwind CSS](https://tailwindcss.com/)** - CSS framework
- **[Pinia](https://pinia.vuejs.org/)** - State management
- **[FingerprintJS](https://fingerprintjs.com/)** - Browser fingerprinting
- **[ApexCharts](https://apexcharts.com/)** - Charts library
- **[Iconify](https://iconify.design/)** - Icons library
- **[Vue3-Flip-Countdown](https://github.com/coskuncay/vue3-flip-countdown)** - Countdown timer

## Project Structure

```
RTPoll
└── frontend
    ├── app
    │   ├── app.vue
    │   ├── assets
    │   │   └── css
    │   │       └── global.css
    │   ├── components
    │   │   ├── ChangeEmail.vue
    │   │   ├── ChangePassword.vue
    │   │   ├── ClosedPollView.vue
    │   │   ├── DeleteAccountBtn.vue
    │   │   ├── DeleteAllPollBtn.vue
    │   │   ├── DeleteClosedPollBtn.vue
    │   │   ├── FloatingNavPanel.vue
    │   │   ├── ForgotPasswordWindow.vue
    │   │   ├── GraphView.vue
    │   │   ├── Loading.vue
    │   │   ├── LogoutBtn.vue
    │   │   ├── marketing
    │   │   │   ├── Footer.vue
    │   │   │   └── Navbar.vue
    │   │   ├── PollCard.vue
    │   │   ├── PollSettings.vue
    │   │   ├── PopupMessage.vue
    │   │   ├── PoweredByFooter.vue
    │   │   ├── ProfileCard.vue
    │   │   └── RunningPollView.vue
    │   ├── composables
    │   │   ├── useApi.js
    │   │   ├── useAuth.js
    │   │   ├── usePopup.js
    │   │   └── useValidation.js
    │   ├── error.vue
    │   ├── layouts
    │   │   ├── dashboard.vue
    │   │   ├── mail-redirect.vue
    │   │   └── marketing.vue
    │   ├── middleware
    │   │   ├── auth.js
    │   │   └── guest.js
    │   ├── pages
    │   │   ├── about.vue
    │   │   ├── dashboard
    │   │   │   ├── create.vue
    │   │   │   ├── index.vue
    │   │   │   ├── poll
    │   │   │   │   └── [id].vue
    │   │   │   └── settings.vue
    │   │   ├── index.vue
    │   │   ├── login.vue
    │   │   ├── poll
    │   │   │   └── [id].vue
    │   │   ├── privacy-policy.vue
    │   │   ├── recover-pass.vue
    │   │   ├── register.vue
    │   │   ├── update-mail.vue
    │   │   └── verify-mail.vue
    │   ├── plugins
    │   │   └── apexcharts.client.js
    │   ├── stores
    │   │   └── publicPoll.js
    │   └── utils
    │       └── formatNumber.js
    ├── nuxt.config.ts
    ├── package.json
    ├── pnpm-lock.yaml
    ├── pnpm-workspace.yaml
    ├── README.md
    └── tsconfig.json

16 directories, 53 files
```

