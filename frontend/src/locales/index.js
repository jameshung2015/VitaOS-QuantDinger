import Vue from 'vue'
import VueI18n from 'vue-i18n'
import storage from 'store'
import moment from 'moment'

// default lang
import enUS from './lang/en-US'

Vue.use(VueI18n)

export const defaultLang = 'en-US'
const supportedLangs = ['en-US', 'zh-CN']

const messages = {
  'en-US': {
    ...enUS
  }
}

const i18n = new VueI18n({
  silentTranslationWarn: true,
  locale: defaultLang,
  fallbackLocale: defaultLang,
  messages
})

const loadedLanguages = [defaultLang]

function setI18nLanguage (lang) {
  i18n.locale = lang
  const html = document.documentElement
  const isRtl = /^ar/i.test(lang)
  if (html) {
    // request.headers['Accept-Language'] = lang
    html.setAttribute('lang', lang)
    html.setAttribute('dir', isRtl ? 'rtl' : 'ltr')
  }
  if (document.body) {
    document.body.setAttribute('dir', isRtl ? 'rtl' : 'ltr')
    document.body.classList.toggle('rtl', isRtl)
  }
  return lang
}

export function loadLanguageAsync (lang = defaultLang) {
  const safeLang = supportedLangs.includes(lang) ? lang : defaultLang
  return new Promise(resolve => {
    // 缓存语言设置
    storage.set('lang', safeLang)
    if (i18n.locale !== safeLang) {
      if (!loadedLanguages.includes(safeLang)) {
        return import(
          /* webpackChunkName: "lang-[request]" */
          /* webpackInclude: /(en-US|zh-CN)\.js$/ */
          `./lang/${safeLang}`
        ).then(msg => {
          const locale = msg.default
          i18n.setLocaleMessage(safeLang, locale)
          loadedLanguages.push(safeLang)
          moment.updateLocale(locale.momentName, locale.momentLocale)
          return setI18nLanguage(safeLang)
        })
      }
      return resolve(setI18nLanguage(safeLang))
    }
    return resolve(safeLang)
  })
}

export function i18nRender (key) {
  return i18n.t(`${key}`)
}

export default i18n
