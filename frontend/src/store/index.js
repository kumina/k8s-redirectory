import Vue from 'vue'
import Vuex from 'vuex'

import mainPageView from './modules/mainPageView'
import api from './modules/api'
import dialogs from './modules/dialogs'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      mainPageView: mainPageView,
      api: api,
      dialogs: dialogs
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })

  return Store
}
