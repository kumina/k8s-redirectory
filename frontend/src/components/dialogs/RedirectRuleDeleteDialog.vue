<template>
  <q-dialog full-width v-model="is_open" :position="position">
    <q-card v-if="redirect_rule != null" class="bg-grey-3 modal">
      <q-card-section class="bg-primary text-white">
        <div class="row flex-center">
          <div class="col">
            <div class="text-h6">DELETE | Redirect Rule</div>
          </div>
          <div class="col-auto">
            <q-icon name="delete" size="35px"/>
          </div>
        </div>
      </q-card-section>
      <q-separator class="toolbarGradient"/>

      <q-card-section>
        <div class="doc-note doc-note--danger">
          <p class="doc-note__title">DANGER ZONE</p>
          <p>
            Once a rule is deleted there is no way to recover it back.
            You will need to create a brand new one with the same values in order to get it back.
          </p>
        </div>
        <br>
        <div class="doc-note doc-note--tip">
          <p class="doc-note__title">QUICK TIP</p>
          <p>
            Once a rule is deleted it will <b>NOT</b> take effect instantly.
            You will need to recompile Hyperscan database and update all the workers.
          </p>
        </div>
      </q-card-section>

      <q-card-section>
        <p class="text-h5">
          Redirect Rule to remove:
        </p>
        <q-card class="text-h6" style="margin-bottom: 10px">
          <div class="row q-item">
            <div class="col-3">
              ID:
            </div>
            <div class="col">
              {{ redirect_rule.id }}
            </div>
          </div>
        </q-card>
        <q-card class="text-h6">
          <div class="row q-item">
            <div class="col-3">
              DESTINATION:
            </div>
            <div class="col">
              {{ redirect_rule.destination_rule.destination_url }}
            </div>
          </div>
        </q-card>
      </q-card-section>

      <q-separator class="separatorGradient"/>
      <q-card-actions>
        <q-btn @click="delete_rule" color="negative" label="DELETE REDIRECT RULE" icon="delete"></q-btn>
        <q-btn @click="close" color="negative" label="CLOSE / CANCEL" flat></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'RedirectRuleDeleteDialog',
  computed: {
    is_open: {
      get: function () {
        return this.$store.state.dialogs.show_delete
      },
      set: function (value) {
        this.$store.commit('dialogs/set_delete', value)
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
    delete_rule () {
      let postData = {
        rule_id: this.redirect_rule.id
      }

      // Make API call
      this.$axios.post(this.$store.state.api.MGMT_RULES_DELETE, postData)
        .then(() => this.handle_response())
        .catch((error) => this.handle_error(error))
    },
    handle_response () {
      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'Successfully deleted rule with id: ' + this.redirect_rule.id,
        icon: 'check',
        actions: [{ icon: 'close', color: 'white' }]
      })
      this.close()
    },
    handle_error (error) {
      let errorData = error.response.data

      this.$q.notify({
        color: 'negative',
        position: 'top',
        message: errorData.error,
        icon: 'report_problem',
        actions: [{ icon: 'close', color: 'white' }]
      })
    },
    close () {
      this.is_open = false
    }
  }
}
</script>

<style scoped lang="stylus">

  .modal
    width 800px !important

</style>
