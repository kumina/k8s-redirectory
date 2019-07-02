<template>
  <div style="width: 100%">
    <q-card style="width: 100%" @mouseleave="lost_focus">
      <div class="row q-item cursor-pointer hoverable" @click="toggle_edit_mode" :class="is_dimmed">
        <div class="col-1" style="max-width: 50px">
          <q-item-label caption>ID</q-item-label>
          <q-item-label class="text-bold">{{ redirectRule.id }}</q-item-label>
        </div>
        <div class="col-1" style="max-width: 50px">
          <q-item-label caption>REGEX</q-item-label>
          <q-item-label class="text-uppercase text-bold" :class="get_color(redirectRule.domain_rule.is_regex)">
            {{ redirectRule.domain_rule.is_regex }}
          </q-item-label>
        </div>
        <div class="col-2">
          <q-item-label caption>DOMAIN</q-item-label>
          <q-item-label class="ellipsis">{{ redirectRule.domain_rule.rule }}</q-item-label>
        </div>

        <div class="col-1" style="max-width: 50px">
          <q-item-label caption>REGEX</q-item-label>
          <q-item-label class="text-uppercase text-bold" :class="get_color(redirectRule.path_rule.is_regex)">
            {{ redirectRule.path_rule.is_regex }}
          </q-item-label>
        </div>
        <div class="col">
          <q-item-label caption>PATH</q-item-label>
          <q-item-label class="ellipsis">{{ redirectRule.path_rule.rule }}</q-item-label>
        </div>

        <div class="col-1" style="max-width: 60px">
          <q-item-label caption>REWRITE</q-item-label>
          <q-item-label class="text-uppercase text-bold" :class="get_color(redirectRule.destination_rule.is_rewrite)">
            {{ redirectRule.destination_rule.is_rewrite }}
          </q-item-label>
        </div>
        <div class="col">
          <q-item-label caption>DESTINATION</q-item-label>
          <q-item-label class="ellipsis">{{ redirectRule.destination_rule.destination_url }}</q-item-label>
        </div>

        <div class="col-1" style="max-width: 50px">
          <q-item-label caption>WEIGHT</q-item-label>
          <q-item-label class="text-black text-bold">{{ redirectRule.weight }}</q-item-label>
        </div>
      </div>
      <q-item v-show="edit_mode" class="absolute absolute-right overlay" style="width: 45%">
        <q-item-section>
          <div class="row" style="height: 100%">
            <div class="col flex flex-center">
              <q-btn @click="toggle_view" color="primary" unelevated class="edge-btn">
                <q-icon left name="visibility"/>
                <div>VIEW</div>
              </q-btn>
            </div>
            <div class="col flex flex-center">
              <q-btn @click="toggle_edit" color="secondary" unelevated class="edge-btn">
                <q-icon left name="edit"/>
                <div>EDIT</div>
              </q-btn>
            </div>
            <div class="col flex flex-center">
              <q-btn @click="toggle_delete" color="negative" unelevated class="edge-btn">
                <q-icon left name="delete"/>
                <div>DELETE</div>
              </q-btn>
            </div>
          </div>
        </q-item-section>
      </q-item>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'RedirectRuleBlock',
  props: ['redirectRule'],
  components: {
  },
  data () {
    return {
      show_view: false,
      show_edit: false,
      show_delete: false,
      edit_mode: false
    }
  },
  computed: {
    is_dimmed () {
      return this.edit_mode ? 'dimmed' : ''
    }
  },
  methods: {
    toggle_view () {
      this.$store.commit('dialogs/set_redirect_rule', this.redirectRule)
      this.$store.commit('dialogs/set_view', true)
    },
    toggle_edit () {
      this.$store.commit('dialogs/set_redirect_rule', this.redirectRule)
      this.$store.commit('dialogs/set_edit', true)
    },
    toggle_delete () {
      this.$store.commit('dialogs/set_redirect_rule', this.redirectRule)
      this.$store.commit('dialogs/set_delete', true)
    },
    toggle_edit_mode () {
      this.edit_mode = !this.edit_mode
    },
    lost_focus () {
      this.edit_mode = false
    },
    get_color (value) {
      return value ? 'text-positive' : 'text-negative'
    }
  }
}
</script>

<style scoped lang="stylus">
  .mr-1
    margin-right 10px

  .edge-btn
    height 100%
    width 100%
    border-radius 0 !important
    opacity 0.9

  .overlay
    padding 0 !important

  .dimmed
    background: rgba(0, 0, 0, 0.5) !important;
</style>
