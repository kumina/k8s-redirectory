const mainPageView = {
  state: {
    redirectRulesOpened: true,
    innerWorkingsOpened: true,
    isRippleOn: false,
    ambiguousRequest: null,
    scrollTo: null
  },
  mutations: {
    setRedirectRuleOpened (state, value) {
      state.redirectRulesOpened = value
    },
    setInnerWorkingsOpened (state, value) {
      state.innerWorkingsOpened = value
    },
    setRipple (state, value) {
      state.isRippleOn = value
    },
    setAmbiguousRequest (state, value) {
      state.ambiguousRequest = value
    },
    setScrollTo (state, value) {
      state.scrollTo = value
    }
  },
  namespaced: true
}

export default mainPageView
