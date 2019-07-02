<template>
  <q-card class="my-card bg-grey-3">
    <q-card-section class="bg-primary text-white">
      <div class="row flex-center">
        <div class="col">
          <div class="text-h6">Redirect Rule Explorer</div>
        </div>
        <div class="col-auto">
          <q-icon name="explore" size="35px"/>
        </div>
      </div>
    </q-card-section>
    <q-separator class="toolbarGradient"/>

    <!-- Filter -->
    <q-card-section>
      <q-card style="width: 100%">
        <q-card-section style="padding-bottom: 0; padding-top: 5px;">
          <div class="row q-item">
            <div class="col text-h5">
              Search Filters
            </div>
            <div class="col-auto">
              <q-btn color="negative" @click="clear_filters()">CLEAR ALL FILTERS</q-btn>
            </div>
          </div>
          <div class="row q-item" style="padding-top: 0;">
            <div class="doc-note col">
              <p>
                If a field is left empty/untouched it will not be included in the filters.
                You can also use a <b>wild card <i class="text-accent"> ( * ) </i></b> in the text fields.
                If you want to search for just <b class="text-accent">*</b> as a character you have to
                escape it like so: <b class="text-accent">\*</b>
              </p>
            </div>
          </div>
        </q-card-section>
        <q-card-section>
          <div class="row q-item">
            <div class="col" style="margin-right: 10px">
              <q-item-label caption>
                ID
              </q-item-label>
              <q-item-label>
                <q-input
                  v-model.number="filter.id"
                  type="number"
                  clearable
                  placeholder="example: 1"
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
            <div class="col" style="margin-right: 10px">
              <q-item-label caption>
                DOMAIN ID
              </q-item-label>
              <q-item-label class="text-black">
                <q-input
                  v-model.number="filter.domain_rule_id"
                  type="number"
                  clearable
                  placeholder="example: 1"
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
            <div class="col" style="margin-right: 10px">
              <q-item-label caption>
                PATH ID
              </q-item-label>
              <q-item-label class="text-black">
                <q-input
                  v-model.number="filter.path_rule_id"
                  type="number"
                  clearable
                  placeholder="example: 1"
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
            <div class="col" style="margin-right: 10px">
              <q-item-label caption>
                DESTINATION ID
              </q-item-label>
              <q-item-label class="text-black">
                <q-input
                  v-model.number="filter.destination_rule_id"
                  type="number"
                  clearable
                  placeholder="example: 1"
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
            <div class="col">
              <q-item-label caption>
                WEIGHT
              </q-item-label>
              <q-item-label class="text-black">
                <q-input
                  v-model.number="filter.weight"
                  type="number"
                  clearable
                  placeholder="example: 100"
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
          </div>

          <div class="row q-item">
            <div class="col-3" style="margin-right: 10px">
              <q-item-label caption>DOMAIN REGEX</q-item-label>
              <q-item-label>
                <q-btn-toggle
                  spread
                  v-model="filter.domain_is_regex"
                  toggle-color="primary"
                  :options="[
                      {label: 'ANY', value: 'any'},
                      {label: 'REGEX', value: 'regex'},
                      {label: 'LITERAL', value: 'literal'}
                     ]"
                />
              </q-item-label>
            </div>
            <div class="col">
              <q-item-label caption>DOMAIN</q-item-label>
              <q-item-label class="ellipsis">
                <q-input
                  v-model.number="filter.domain"
                  placeholder="example: example.com"
                  clearable
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
          </div>

          <div class="row q-item">
            <div class="col-3" style="margin-right: 10px">
              <q-item-label caption>PATH REGEX</q-item-label>
              <q-item-label>
                <q-btn-toggle
                  spread
                  v-model="filter.path_is_regex"
                  toggle-color="primary"
                  :options="[
                      {label: 'ANY', value: 'any'},
                      {label: 'REGEX', value: 'regex'},
                      {label: 'LITERAL', value: 'literal'}
                     ]"
                />
              </q-item-label>
            </div>
            <div class="col">
              <q-item-label caption>PATH</q-item-label>
              <q-item-label class="ellipsis">
                <q-input
                  v-model.number="filter.path"
                  placeholder="example: /test/path"
                  clearable
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
          </div>

          <div class="row q-item">
            <div class="col-3" style="margin-right: 10px">
              <q-item-label caption>DESTINATION REWRITE</q-item-label>
              <q-item-label>
                <q-btn-toggle
                  spread
                  v-model="filter.destination_is_rewrite"
                  toggle-color="primary"
                  :options="[
                      {label: 'ANY', value: 'any'},
                      {label: 'REWRITE', value: 'rewrite'},
                      {label: 'LITERAL', value: 'literal'}
                     ]"
                />
              </q-item-label>
            </div>
            <div class="col">
              <q-item-label caption>DESTINATION</q-item-label>
              <q-item-label class="ellipsis">
                <q-input
                  v-model.number="filter.destination"
                  placeholder="example: https://dest.com/new/path"
                  clearable
                  filled dense
                  style="width: 100%"
                />
              </q-item-label>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-card-section>

    <!-- CREATE RULE -->
    <q-card-section>
      <div class="row">
        <div class="col-auto">
          <q-btn @click="apply_filters()" color="primary" icon="search" label="APPLY FILTERS"></q-btn>
        </div>
        <div class="col" style="margin-left: 10px">
          <q-pagination
            v-model="page.current"
            color="primary"
            :max="page.total"
            :max-pages="4"
            :boundary-numbers="true"
            :direction-links="true"
            @input="page_changed()"
            style="max-width: 100%"
          >
          </q-pagination>
        </div>
        <div class="col-auto">
          <div class="row justify-end">
            <div class="col-auto">
              <q-btn color="primary" icon="add" label="CREATE NEW REDIRECT RULE" @click="toggle_create"
                     style="margin-right: 10px"></q-btn>
            </div>
            <div class="col-auto">
              <q-btn color="secondary" icon="refresh" label="REFRESH PAGES"
                     @click="page_changed(skipCache=true)"></q-btn>
            </div>
          </div>
        </div>
      </div>
    </q-card-section>

    <q-card-section>
      <div v-if="current_page_data.length > 0">
        <div class="row flex flex-center" v-for="redirectRule in current_page_data" v-bind:key="redirectRule.id">
          <RedirectRuleBlock class="row-item" :redirect-rule="redirectRule"></RedirectRuleBlock>
        </div>
      </div>
      <div v-else>
        <div class="row flex flex-center text-h6">
          No results with specified filters!
        </div>
      </div>
    </q-card-section>

    <q-separator class="separatorGradient"/>
  </q-card>
</template>

<script>
import RedirectRuleBlock from '../blocks/RedirectRuleBlock.vue'

export default {
  name: 'RedirectRuleExplorer',
  components: {
    RedirectRuleBlock
  },
  data () {
    return {
      page: {
        current: 1,
        size: 10,
        total: 2
      },
      filter: {
        id: null,
        domain: '',
        domain_is_regex: 'any',
        domain_rule_id: null,
        path: '',
        path_is_regex: 'any',
        path_rule_id: null,
        destination: '',
        destination_is_rewrite: 'any',
        destination_rule_id: null,
        weight: null
      },
      current_page_data: [],
      cache: {
        data: {},
        max_size: 25
      }
    }
  },
  created () {
    this.page_changed()
  },
  methods: {
    toggle_create () {
      this.$store.commit('dialogs/set_redirect_rule', this.redirectRule)
      this.$store.commit('dialogs/set_create', true)
    },
    apply_filters () {
      // Clear cache
      this.cache.data = {}

      this.page_changed()
    },
    page_changed (skipCache = false) {
      if (!skipCache && this.page.current in this.cache.data) {
        this.current_page_data = this.cache.data[this.page.current]
        return
      }

      let postData = {
        page_number: this.page.current,
        page_size: this.page.size
      }

      let filters = this.get_filters()
      if (Object.keys(filters).length !== 0) {
        postData.filter = filters
      }

      this.$axios.post(this.$store.state.api.MGMT_RULES_GET_PAGE, postData)
        .then((response) => this.load_page_items(response.data))
        .catch(() => {
          if (this.page.current > 1) {
            this.page.current = 1
            this.page_changed(skipCache = true)
          } else {
            this.page.total = 1
            this.current_page_data = {}
          }
        })
    },
    load_page_items (data) {
      this.current_page_data = data.data
      this.page.total = data.page.total_pages

      // Append to cache and if needed clear cache
      if (Object.keys(this.cache.data).length > this.cache.max_size) {
        let toRemove = Object.keys(this.cache.data).sort((a, b) => a - b)[0]
        delete this.cache.data[toRemove]

        // Debug
        console.log('Cache overflow! Page to remove from cache: ' + toRemove)
      }

      this.cache.data[this.page.current] = data.data
    },
    get_filters () {
      let filters = {}

      if (this.filter.id != null && this.filter.id !== '') {
        filters.redirect_rule_id = this.filter.id
      }
      if (this.filter.domain_rule_id != null && this.filter.domain_rule_id !== '') {
        filters.domain_rule_id = this.filter.domain_rule_id
      }
      if (this.filter.path_rule_id != null && this.filter.path_rule_id !== '') {
        filters.path_rule_id = this.filter.path_rule_id
      }
      if (this.filter.destination_rule_id != null && this.filter.destination_rule_id !== '') {
        filters.destination_rule_id = this.filter.destination_rule_id
      }
      if (this.filter.weight != null && this.filter.weight !== '') {
        filters.weight = this.filter.weight
      }

      if (this.filter.domain_is_regex !== 'any') {
        filters.domain_is_regex = this.get_bool_from_str(this.filter.domain_is_regex)
      }
      if (this.filter.path_is_regex !== 'any') {
        filters.path_is_regex = this.get_bool_from_str(this.filter.path_is_regex)
      }
      if (this.filter.destination_is_rewrite !== 'any') {
        filters.destination_is_rewrite = this.get_bool_from_str(this.filter.destination_is_rewrite)
      }

      if (this.filter.domain != null && this.filter.domain !== '') {
        filters.domain = this.filter.domain
      }
      if (this.filter.path != null && this.filter.path !== '') {
        filters.path = this.filter.path
      }
      if (this.filter.destination != null && this.filter.destination !== '') {
        filters.destination = this.filter.destination
      }

      return filters
    },
    get_bool_from_str (str) {
      return !(str === 'literal')
    },
    clear_filters () {
      this.filter.id = null
      this.filter.domain = ''
      this.filter.domain_is_regex = 'any'
      this.filter.domain_rule_id = null
      this.filter.path = ''
      this.filter.path_is_regex = 'any'
      this.filter.path_rule_id = null
      this.filter.destination = ''
      this.filter.destination_is_rewrite = 'any'
      this.filter.destination_rule_id = null
      this.filter.weight = null

      this.apply_filters()
    }
  }
}
</script>

<style lang="stylus" scoped>
  .row-item
    margin-bottom 5px !important
</style>
