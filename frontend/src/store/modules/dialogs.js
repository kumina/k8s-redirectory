const dialogs = {
  state: {
    redirectRule: null,
    configuration: null,
    show_view: false,
    show_edit: false,
    show_delete: false,
    show_create: false,
    show_configuration: false,
    show_user_guide: false
  },
  mutations: {
    set_redirect_rule (state, value) {
      state.redirectRule = value
    },
    set_configuration (state, value) {
      state.configuration = value
    },
    set_view (state, value) {
      state.show_view = value
    },
    set_edit (state, value) {
      state.show_edit = value
    },
    set_delete (state, value) {
      state.show_delete = value
    },
    set_create (state, value) {
      state.show_create = value
    },
    set_show_configuration (state, value) {
      state.show_configuration = value
    },
    set_user_guide (state, value) {
      state.show_user_guide = value
    }
  },
  namespaced: true
}

export default dialogs
