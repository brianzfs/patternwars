/*!
 * Farbmodus-Umschalter (hell / dunkel / System)
 * Basiert auf dem Beispiel aus der Bootstrap-Dokumentation:
 * https://getbootstrap.com/docs/5.3/customize/color-modes/#javascript
 */

(() => {
    'use strict'

    const getStoredTheme = () => {
        try {
            return localStorage.getItem('theme')
        } catch {
            return null
        }
    }

    const setStoredTheme = theme => {
        try {
            localStorage.setItem('theme', theme)
        } catch {
            // Speichern nicht möglich (z. B. privater Modus), Auswahl gilt dann nur für diese Seite
        }
    }

    // Ohne gespeicherte Auswahl wird das System-Design verwendet
    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme()
        return ['light', 'dark', 'auto'].includes(storedTheme) ? storedTheme : 'auto'
    }

    const prefersDark = () => window.matchMedia('(prefers-color-scheme: dark)').matches

    const setTheme = theme => {
        if (theme === 'auto') {
            document.documentElement.setAttribute('data-bs-theme', prefersDark() ? 'dark' : 'light')
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme)
        }
    }

    setTheme(getPreferredTheme())

    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector('#bd-theme')

        if (!themeSwitcher) {
            return
        }

        const themeSwitcherText = document.querySelector('#bd-theme-text')
        const activeThemeIcon = document.querySelector('.theme-icon-active')
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
        const iconOfActiveBtn = btnToActive.querySelector('.bi').dataset.themeIcon

        document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
        })

        btnToActive.classList.add('active')
        btnToActive.setAttribute('aria-pressed', 'true')
        activeThemeIcon.className = `bi ${iconOfActiveBtn} theme-icon-active`
        themeSwitcher.setAttribute('aria-label', `${themeSwitcherText.textContent} (${btnToActive.textContent.trim()})`)

        if (focus) {
            themeSwitcher.focus()
        }
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (getPreferredTheme() === 'auto') {
            setTheme('auto')
        }
    })

    window.addEventListener('DOMContentLoaded', () => {
        showActiveTheme(getPreferredTheme())

        document.querySelectorAll('[data-bs-theme-value]').forEach(toggle => {
            toggle.addEventListener('click', () => {
                const theme = toggle.getAttribute('data-bs-theme-value')
                setStoredTheme(theme)
                setTheme(theme)
                showActiveTheme(theme, true)
            })
        })
    })
})()
