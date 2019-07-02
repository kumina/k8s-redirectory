<template>
  <q-card style="width: 100%">
    <q-item>
      <q-item-section avatar>
        <q-item-label caption>ID</q-item-label>
        <q-item-label>{{ redirectRule.id }}</q-item-label>
      </q-item-section>

      <q-item-section avatar>
        <q-item-label caption>DOMAIN ID</q-item-label>
        <q-item-label>{{ redirectRule.domain_rule.id }}</q-item-label>
      </q-item-section>

      <q-item-section>
        <q-item-label caption>PATH</q-item-label>
        <q-item-label>{{ redirectRule.path_rule.rule }}</q-item-label>
      </q-item-section>

      <q-item-section style="max-width: 50px">
        <q-item-label caption>REGEX</q-item-label>
        <q-item-label :class="get_color(redirectRule.path_rule.is_regex)">
          {{ redirectRule.path_rule.is_regex }}
        </q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-item-label caption>WEIGHT</q-item-label>
        <q-item-label class="text-black">{{ redirectRule.weight }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-card>
</template>

<script>
export default {
  name: 'RuleBlock',
  props: ['redirectRule'],
  methods: {
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

<style scoped lang="stylus">
  .mt
    margin-top 10px
</style>
