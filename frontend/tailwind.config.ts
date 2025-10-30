import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#6366f1',
          dark: '#4f46e5'
        },
        bg: {
          primary: '#1a2332',
          secondary: '#2d3748',
          card: '#374151'
        },
        textc: {
          primary: '#f9fafb',
          secondary: '#9ca3af'
        },
        status: {
          success: '#10b981',
          error: '#ef4444',
          warning: '#f59e0b'
        }
      },
      borderRadius: {
        xl: '12px'
      }
    }
  },
  plugins: []
}

export default config


