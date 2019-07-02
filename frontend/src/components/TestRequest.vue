<template>
  <q-card class="my-card bg-grey-3 shadow-3">
    <q-card-section class="bg-primary text-white">
      <div class="row flex-center">
        <div class="col">
          <div class="text-h6">Test request</div>
        </div>
        <div class="col-auto">
          <q-icon name="http" size="35px"/>
        </div>
      </div>
    </q-card-section>
    <q-separator class="toolbarGradient"/>

    <q-card-section>
      <div class="row flex-center">
        <div class="col">
          <q-input input-class="text-h6" v-model="test_request" filled placeholder="example.com/test/path/1">
            <template v-slot:prepend>
              https://
            </template>
          </q-input>
        </div>
        <div class="col-auto" style="margin-left: 10px;">
          <q-btn color="primary" @click="testRequest()">
            <q-icon left size="3.4em" name="send"/>
            <div>TEST</div>
          </q-btn>
        </div>
      </div>
    </q-card-section>

    <q-card-section v-if="is_loaded">
      <q-separator spaced></q-separator>
      <div class="row" style="margin-bottom: 5px;">
        <div class="flex flex-center col-5">
          DOMAINS MATCHED
        </div>
        <div class="flex flex-center col">
          RULES MATCHED
        </div>
      </div>
      <div class="row">
        <!--Domain Section-->
        <div class="col-5" v-if="Object.keys(domains_matched).length > 0">
          <div v-for="domain in domains_matched" v-bind:key="domain.id">
            <DomainBlock class="display-input" :domain="domain"></DomainBlock>
          </div>
        </div>
        <div v-else class="col-5 flex flex-center text-negative">
          No domains matched
        </div>

        <!--Rule Section-->
        <div class="col" v-if="Object.keys(rules_matched).length > 0">
          <div v-for="redirectRule in rules_matched" v-bind:key="redirectRule.id">
            <RuleBlock class="display-input" :redirectRule="redirectRule"></RuleBlock>
          </div>
        </div>
        <div v-else class="col flex flex-center text-negative">
          No rules matched
        </div>
      </div>

      <q-separator spaced></q-separator>

      <div class="row flex flex-center" style="margin-bottom: 5px">
        FINAL RESULT
      </div>
      <div v-if="final_rule_match != null" class="row flex flex-center">
        <RedirectRuleBlock class="display-input" :redirectRule="final_rule_match"></RedirectRuleBlock>
      </div>
      <div v-else class="row flex flex-center text-negative">
        No final result
      </div>

      <q-separator spaced></q-separator>

      <div class="row" style="margin-bottom: 5px">
        <div class="col flex flex-center">
          DOMAIN SEARCH QUERIES
        </div>
        <div class="col flex flex-center">
          RULE SEARCH QUERIES
        </div>
      </div>

      <div class="row">
        <div class="col">
          <q-card v-for="domain_search in domain_search_queries" class="display-input search-block flex flex-center"
                  v-bind:key="domain_search">
            <b>
              {{ domain_search }}
            </b>
          </q-card>
        </div>
        <div class="col">
          <div v-if="rules_search_queries.length > 0">
            <q-card v-for="rule_search in rules_search_queries" class="display-input search-block flex flex-center"
                    v-bind:key="rule_search" style="width: 100%">
              <b>
                {{ rule_search }}
              </b>
            </q-card>
          </div>
          <div v-else class="flex flex-center text-negative">
            No rule search queries
          </div>
        </div>
      </div>

      <q-separator spaced></q-separator>

      <div class="row" style="margin-bottom: 5px">
        <div class="col flex flex-center">
          IS REQUEST AMBIGUOUS
        </div>
        <div class="col flex flex-center">
          TIME FOR HYPERSCAN SEARCH
        </div>
      </div>

      <div class="row">
        <div class="col">
          <q-card class="display-input search-block">
            <div class="row">
              <div class="col">
                All matched rules have the same weight:
              </div>
              <div class="col-1" style="margin-right: 5px">
                <span v-if="is_request_ambiguous != null" :class="get_color(is_request_ambiguous)">
                  {{ is_request_ambiguous }}
                </span>
                <span v-else class="text-negative">
                  none
                </span>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col">
          <q-card class="display-input search-block" style="width: 100%">
            <div class="row">
              <div class="col">
                {{ search_time }}
              </div>
              <div class="col-2">
                SECONDS
              </div>
            </div>
          </q-card>
        </div>
      </div>
    </q-card-section>
    <q-card-section v-else>
      <div class="flex flex-center text-h6">
        Data will appear here!
      </div>
    </q-card-section>

    <q-separator class="separatorGradient"/>
    <q-card-actions>
      <q-btn color="negative" @click="clear()">CLEAR</q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
import DomainBlock from './blocks/DomainBlock.vue'
import RuleBlock from './blocks/RuleBlock.vue'
import RedirectRuleBlock from './blocks/RedirectRuleBlock.vue'

export default {
  name: 'TestRequest',
  components: {
    DomainBlock, RuleBlock, RedirectRuleBlock
  },
  data () {
    return {
      test_request: 'example.com/test/path',
      is_loaded: false,

      domains_matched: [],
      domain_search_queries: [],
      rules_matched: [],
      rules_search_queries: [],
      final_rule_match: null,
      is_request_ambiguous: null,
      search_time: null
    }
  },
  computed: {
    ambiguousRequest () {
      return this.$store.state.mainPageView.ambiguousRequest
    }
  },
  watch: {
    ambiguousRequest (newVal, oldVal) {
      if (newVal === null) {
        return
      }

      this.test_request = newVal
      this.$store.commit('mainPageView/setAmbiguousRequest', null)
      this.testRequest()
    }
  },
  methods: {
    testRequest () {
      // Check input
      if (this.test_request === '') {
        return
      }

      // Configure data to send
      let sendTestRequest = this.test_request
      if (!this.test_request.startsWith('https://') && !this.test_request.startsWith('http://')) {
        sendTestRequest = 'https://' + sendTestRequest
      }

      let postData = {
        request_url: sendTestRequest
      }

      // Make API call
      this.$axios.post(this.$store.state.api.MGMT_RULES_TEST, postData)
        .then((response) => this.handle_test_response(response.data))
        .catch((error) => {
          let errorData = error.response.data

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Loading failed! ' + errorData.error,
            icon: 'report_problem'
          })
        })
    },
    handle_test_response (data) {
      this.domains_matched = data.domain_rules
      this.rules_matched = data.redirect_rules

      let finalId = data.search_data.final_result_id
      this.final_rule_match = this.rules_matched[finalId]

      this.domain_search_queries = [data.search_data.domain_search]
      this.rules_search_queries = data.search_data.rule_searches

      this.is_request_ambiguous = data.search_data.is_ambiguous
      this.search_time = data.search_data.time

      this.is_loaded = true
      console.log(data)
    },
    clear () {
      this.is_loaded = false
      this.domains_matched = []
      this.rules_matched = []
      this.final_rule_match = null
    },
    get_color (value) {
      if (value) {
        return 'text-green'
      } else {
        return 'text-red'
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
  .my-card
    width 90%
    margin-left 5%
    margin-right 5%

  .display-input
    width 95%
    margin-bottom 5px !important

  .search-block
    padding-top 5px
    padding-bottom 5px
    padding-left 15px
</style>
