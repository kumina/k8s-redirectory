<template>
  <q-page class="flex-block">
    <!-- DIALOGS -->
    <RedirectRuleViewDialog></RedirectRuleViewDialog>
    <RedirectRuleCreateDialog></RedirectRuleCreateDialog>
    <RedirectRuleDeleteDialog></RedirectRuleDeleteDialog>
    <RedirectRuleEditDialog></RedirectRuleEditDialog>
    <ConfigurationViewDialog></ConfigurationViewDialog>
    <UserGuideDialog></UserGuideDialog>

    <br>
    <TestRequest id="test_req" v-ripple:purple.center="isRippleOn"></TestRequest>
    <br>

    <q-expansion-item
      :duration=100
      v-model="is_rr_opened"
      switch-toggle-side
      expand-separator
      label="Redirect Rule settings"
      caption="Provides CRUD functionality for the Redirect Rules"
      class="box shadow-3 scroll overflow-hidden"
      icon="assignment"
      header-class="text-h5 bg-grey-3"
    >
<!--      <br>-->
      <RedirectRuleExplorer id="rr_search" v-ripple:purple.center="isRippleOn"
                          class="box-shadow"></RedirectRuleExplorer>
      <br>
      <RedirectRuleBulkImport id="rr_bulk" v-ripple:purple.center="isRippleOn"></RedirectRuleBulkImport>
    </q-expansion-item>
    <br>
    <q-expansion-item
      :duration=100
      v-model="is_iw_opened"
      switch-toggle-side
      expand-separator
      label="Inner workings settings"
      caption="Hyperscan databases, workers and more"
      class="box shadow-3 scroll overflow-hidden"
      icon="settings"
      header-class="text-h5 bg-grey-3"
    >
<!--      <br>-->
      <Workers id="iw_worker" v-ripple:purple.center="isRippleOn" class="box-shadow"></Workers>
      <br>
      <AmbiguousRequests id="iw_amb_req" v-ripple:purple.center="isRippleOn"></AmbiguousRequests>
    </q-expansion-item>
    <br>
    <br>
  </q-page>
</template>

<script>
import TestRequest from '../components/TestRequest.vue'

import RedirectRuleExplorer from '../components/redirect_rules/RedirectRuleExplorer.vue'
import RedirectRuleBulkImport from '../components/redirect_rules/RedirectRuleBulkImport.vue'

import Workers from '../components/inner_workings/Workers.vue'
import AmbiguousRequests from '../components/inner_workings/AmbiguousRequests.vue'

import RedirectRuleViewDialog from '../components/dialogs/RedirectRuleViewDialog.vue'
import RedirectRuleEditDialog from '../components/dialogs/RedirectRuleEditDialog.vue'
import RedirectRuleDeleteDialog from '../components/dialogs/RedirectRuleDeleteDialog.vue'
import RedirectRuleCreateDialog from '../components/dialogs/RedirectRuleCreateDialog.vue'
import ConfigurationViewDialog from '../components/dialogs/ConfigurationViewDialog.vue'
import UserGuideDialog from '../components/dialogs/UserGuideDialog.vue'

export default {
  name: 'PageIndex',
  components: {
    TestRequest,
    RedirectRuleExplorer,
    RedirectRuleBulkImport,
    Workers,
    AmbiguousRequests,
    RedirectRuleViewDialog,
    RedirectRuleCreateDialog,
    RedirectRuleDeleteDialog,
    RedirectRuleEditDialog,
    ConfigurationViewDialog,
    UserGuideDialog
  },
  computed: {
    is_rr_opened: {
      get: function () {
        return this.$store.state.mainPageView.redirectRulesOpened
      },
      set: function (value) {
        this.$store.commit('mainPageView/setRedirectRuleOpened', value)
      }
    },
    is_iw_opened: {
      get: function () {
        return this.$store.state.mainPageView.innerWorkingsOpened
      },
      set: function (value) {
        this.$store.commit('mainPageView/setInnerWorkingsOpened', value)
      }
    },
    isRippleOn () {
      return this.$store.state.mainPageView.isRippleOn
    }
  },
  data () {
    return {
      redirectRulesOpened: false,
      innerWorkingsOpened: false
    }
  }
}
</script>

<style lang="stylus" scoped>
  .box
    width 90%
    margin-left 5%
    margin-right 5%

  .box-shadow
    box-shadow 0 1px 8px rgba(0, 0, 0, 0.2), 0 3px 4px rgba(0, 0, 0, 0.14), 0 3px 3px -2px rgba(0, 0, 0, 0.12) !important
</style>
