<template>
  <q-dialog full-width v-model="is_open" :position="position">
    <q-card v-if="configuration != null" class="bg-grey-3 modal">
      <q-card-section class="bg-primary text-white">
        <div class="row flex-center">
          <div class="col">
            <div class="text-h6">VIEW | Pod Configuration</div>
          </div>
          <div class="col-auto">
            <q-icon name="visibility" size="35px"/>
          </div>
        </div>
      </q-card-section>
      <q-separator class="toolbarGradient"/>

      <q-card-section>
        <vue-json-pretty
          :path="'res'"
          :data="configuration"
        >
        </vue-json-pretty>
      </q-card-section>

      <q-separator class="separatorGradient"/>
      <q-card-actions>
        <q-btn v-close-popup color="negative" label="CLOSE / CANCEL" flat></q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty'

export default {
  name: 'ConfigurationViewDialog',
  components: {
    VueJsonPretty
  },
  computed: {
    is_open: {
      get: function () {
        return this.$store.state.dialogs.show_configuration
      },
      set: function (value) {
        this.$store.commit('dialogs/set_show_configuration', value)
      }
    },
    configuration () {
      return this.$store.state.dialogs.configuration
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
  /*.modal*/
  /*  width 800px !important*/
</style>
