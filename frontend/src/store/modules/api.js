// const BASE_URL = 'http://0.0.0.0:8001'
const BASE_URL = ''
const MGMT_URL = BASE_URL + '/management'
const STATUS_URL = BASE_URL + '/status'
const API_DOC_URL = BASE_URL + '/redirectory-doc'

const api = {
  state: {
    API_DOC_URL: API_DOC_URL,

    MGMT_DB_COMPILE: MGMT_URL + '/database/compile',
    MGMT_DB_COMPILE_TEST: MGMT_URL + '/database/compile_test',
    MGMT_DB_VERSION: MGMT_URL + '/database/version',
    MGMT_DB_RELOAD_MANAGEMENT: MGMT_URL + '/database/reload_management',
    MGMT_DB_RELOAD_WORKERS: MGMT_URL + '/database/reload_workers',
    MGMT_DB_RELOAD_WORKER: MGMT_URL + '/database/reload_worker',

    MGMT_KUBERNETES_GET_MANAGEMENT: MGMT_URL + '/kubernetes/get_management',
    MGMT_KUBERNETES_GET_WORKERS: MGMT_URL + '/kubernetes/get_workers',

    MGMT_RULES_ADD: MGMT_URL + '/rules/add',
    MGMT_RULES_DELETE: MGMT_URL + '/rules/delete',
    MGMT_RULES_GET: MGMT_URL + '/rules/get',
    MGMT_RULES_GET_PAGE: MGMT_URL + '/rules/get_page',
    MGMT_RULES_UPDATE: MGMT_URL + '/rules/update',
    MGMT_RULES_TEST: MGMT_URL + '/rules/test',
    MGMT_RULES_BULK_IMPORT: MGMT_URL + '/rules/bulk_import',

    MGMT_AMBIGUOUS_ADD: MGMT_URL + '/ambiguous/add',
    MGMT_AMBIGUOUS_LIST: MGMT_URL + '/ambiguous/list',
    MGMT_AMBIGUOUS_DELETE: MGMT_URL + '/ambiguous/delete',

    STATUS_GET_NODE_CONFIG: STATUS_URL + '/get_node_configuration',
    STATUS_HEALTH_CHECK: STATUS_URL + '/health_check',
    STATUS_READINESS_CHECK: STATUS_URL + '/readiness_check'
  },
  namespaced: true
}

export default api
