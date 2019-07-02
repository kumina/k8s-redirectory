<template>
  <q-dialog full-width v-model="is_open" :position="position">
    <q-card v-if="redirect_rule != null" class="bg-grey-3 modal">
      <q-card-section class="bg-primary text-white">
        <div class="row flex-center">
          <div class="col">
            <div class="text-h6">VIEW | Redirect Rule</div>
          </div>
          <div class="col-auto">
            <q-icon name="visibility" size="35px"/>
          </div>
        </div>
      </q-card-section>
      <q-separator class="toolbarGradient"/>

      <q-card-section>
        <q-card class="text-h6">
          <div class="row q-item">
            <div class="col-3">
              ID:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.id }}
            </div>
            <div class="col-3">
              WEIGHT:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.weight }}
            </div>
          </div>
        </q-card>
        <br>
        <q-card class="text-h6">
          <div class="row q-item">
            <div class="col-3">
              DOMAIN ID:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.domain_rule.id }}
            </div>
            <div class="col-3">
              IS REGEX:
            </div>
            <div class="col text-bold text-primary text-uppercase" :class="get_color(redirect_rule.domain_rule.is_regex)">
              {{ redirect_rule.domain_rule.is_regex }}
            </div>
          </div>
          <div class="row q-item">
            <div class="col-3">
              DOMAIN:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.domain_rule.rule }}
            </div>
          </div>
        </q-card>
        <br>
        <q-card class="text-h6">
          <div class="row q-item">
            <div class="col-3">
              PATH ID:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.path_rule.id }}
            </div>
            <div class="col-3">
              IS REGEX:
            </div>
            <div class="col text-bold text-primary text-uppercase" :class="get_color(redirect_rule.path_rule.is_regex)">
              {{ redirect_rule.path_rule.is_regex }}
            </div>
          </div>
          <div class="row q-item">
            <div class="col-3">
              PATH:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.path_rule.rule }}
            </div>
          </div>
        </q-card>
        <br>
        <q-card class="text-h6">
          <div class="row q-item">
            <div class="col-3">
              DESTINATION ID:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.destination_rule.id }}
            </div>
            <div class="col-3">
              IS REWRITE:
            </div>
            <div class="col text-bold text-primary text-uppercase" :class="get_color( redirect_rule.destination_rule.is_rewrite )">
              {{ redirect_rule.destination_rule.is_rewrite }}
            </div>
          </div>
          <div class="row q-item">
            <div class="col-3">
              DESTINATION:
            </div>
            <div class="col text-bold text-primary">
              {{ redirect_rule.destination_rule.destination_url }}
            </div>
          </div>
        </q-card>
      </q-card-section>

      <q-separator class="separatorGradient"/>
      <q-card-actions>
        <q-btn v-close-popup color="negative" label="CLOSE / CANCEL" flat></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'RedirectRuleViewDialog',
  computed: {
    is_open: {
      get: function () {
        return this.$store.state.dialogs.show_view
      },
      set: function (value) {
        this.$store.commit('dialogs/set_view', value)
      }
    },
    redirect_rule () {
      return this.$store.state.dialogs.redirectRule
    }
  },
  data () {
    return {
      position: 'right'
    }
  },
  methods: {
    close () {
      this.is_open = false
    },
    get_color (value) {
      return value ? 'text-positive' : 'text-negative'
    }
  }
}
</script>

<style scoped lang="stylus">

.modal
  width 800px !important

</style>
