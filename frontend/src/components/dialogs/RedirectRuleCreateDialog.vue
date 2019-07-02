<template>
  <q-dialog @hide="close()" full-width v-model="is_open" :position="position">
    <q-card class="bg-grey-3 modal">
      <q-card-section class="bg-primary text-white">
        <div class="row flex-center">
          <div class="col">
            <div class="text-h6">CREATE | Redirect Rule</div>
          </div>
          <div class="col-auto">
            <q-icon name="add" size="35px"/>
          </div>
        </div>
      </q-card-section>

      <q-separator class="toolbarGradient"/>

      <q-card-section>
        <div class="doc-note doc-note--tip">
          <p class="doc-note__title">QUICK TIP</p>
          <p>
            Once a new rule is created it will <b>NOT</b> take effect instantly.
            You will need to recompile Hyperscan database and update all the workers.
          </p>
        </div>
        <br>

        <div class="row">
          <div class="col">
            <q-input clearable input-class="text-h6" v-model="domain" filled label="DOMAIN" lazy-rules
                     :error="!is_domain_valid" :error-message="domain_err_msg" bottom-slots
                     @blur="domain_touched = true"
                     placeholder="example.com" hint="At least 3 characters"/>
          </div>
          <div class="col-2 flex flex-center" style="margin-left: 10px">
            <q-toggle
              :label="domain_is_regex"
              v-model="domain_is_regex"
              checked-icon="code"
              unchecked-icon="text_format"
              false-value="LITERAL"
              true-value="REGEX"
              color="secondary"
              class="toggle-label"
            />
          </div>
        </div>
        <br>
        <div class="row">
          <div class="col">
            <q-input clearable input-class="text-h6" v-model="path" filled label="PATH" lazy-rules
                     :error="!is_path_valid" :error-message="path_err_msg" bottom-slots
                     @blur="path_touched = true"
                     placeholder="/test/path/.*" hint="At least 1 character"/>
          </div>
          <div class="col-2 flex flex-center" style="margin-left: 10px">
            <q-toggle
              :label="path_is_regex"
              v-model="path_is_regex"
              checked-icon="code"
              unchecked-icon="text_format"
              false-value="LITERAL"
              true-value="REGEX"
              color="secondary"
              class="toggle-label"
            />
          </div>
        </div>
        <br>
        <div class="row">
          <div class="col">
            <q-input clearable input-class="text-h6" v-model="destination" filled label="DESTINATION" lazy-rules
                     :error="!is_destination_valid" :error-message="destination_err_msg" bottom-slots
                     @blur="destination_touched = true"
                     placeholder="https://example.com/new/test/path" hint="At least 10 characters"/>
          </div>
          <div class="col-2 flex flex-center" style="margin-left: 10px">
            <q-toggle
              :label="destination_is_rewrite"
              v-model="destination_is_rewrite"
              checked-icon="code"
              unchecked-icon="text_format"
              false-value="LITERAL"
              true-value="REWRITE"
              color="secondary"
              class="toggle-label"
            />
          </div>
        </div>
        <br>
        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col-2" style="margin-right: 20px">
                <q-input label="WEIGHT" input-class="text-h6" type="number" v-model="weight" filled/>
              </div>
              <div class="col flex flex-center">
                <q-slider v-model="weight" :min="0" :max="200" :step="5" markers snap color="secondary"/>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>

      <q-separator class="separatorGradient"/>
      <q-card-actions>
        <q-btn color="green" @click="create()">CREATE</q-btn>
        <q-btn color="negative" @click="clear()">CLEAR</q-btn>
        <q-btn @click="close" color="negative" label="CLOSE / CANCEL" flat></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: 'RedirectRuleCreateDialog',
  computed: {
    is_open: {
      get: function () {
        return this.$store.state.dialogs.show_create
      },
      set: function (value) {
        this.$store.commit('dialogs/set_create', value)
      }
    },
    redirect_rule () {
      return this.$store.state.dialogs.redirectRule
    },
    is_domain_valid () {
      return this.domain.length >= 3 || !this.domain_touched
    },
    is_path_valid () {
      return this.path.length >= 1 || !this.path_touched
    },
    is_destination_valid () {
      return this.destination.length >= 10 || !this.destination_touched
    }
  },
  data () {
    return {
      position: 'right',

      domain: '',
      domain_err_msg: 'Domain must be at least 3 characters',
      domain_is_regex: 'LITERAL',
      domain_touched: false,

      path: '',
      path_err_msg: 'Path must be at least 1 character',
      path_is_regex: 'LITERAL',
      path_touched: false,

      destination: '',
      destination_err_msg: 'Destination must be at least 10 characters',
      destination_is_rewrite: 'LITERAL',
      destination_touched: false,

      weight: 100
    }
  },
  methods: {
    create () {
      // Check
      this.domain_touched = true
      this.path_touched = true
      this.destination_touched = true

      if (!this.is_domain_valid || !this.is_path_valid || !this.is_destination_valid) {
        console.log('Some imputs are not valid')
        return
      }

      // Gather data
      let postData = {
        domain: this.domain,
        domain_is_regex: this.convert_to_bool(this.domain_is_regex),
        path: this.path,
        path_is_regex: this.convert_to_bool(this.path_is_regex),
        destination: this.destination,
        destination_is_rewrite: this.convert_to_bool(this.destination_is_rewrite),
        weight: this.weight
      }

      // Make API call
      this.$axios.post(this.$store.state.api.MGMT_RULES_ADD, postData)
        .then((response) => this.handle_response(response))
        .catch((error) => this.handle_error(error))
    },
    handle_response (response) {
      let data = response.data

      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'New rule created with id: ' + data.new_rule.id,
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
    clear () {
      this.domain = ''
      this.domain_is_regex = 'LITERAL'
      this.domain_touched = false

      this.path = ''
      this.path_is_regex = 'LITERAL'
      this.path_touched = false

      this.destination = ''
      this.destination_is_rewrite = 'LITERAL'
      this.destination_touched = false

      this.weight = 100
    },
    convert_to_bool (inStr) {
      return inStr !== 'LITERAL'
    },
    close () {
      this.clear()
      this.is_open = false
    }
  }
}
</script>

<style scoped lang="stylus">
  .modal
    width 800px !important

  .my-card
    width 100%

  .input-label
    margin auto
    font-weight bold

  .toggle-label
    font-weight bold
</style>
