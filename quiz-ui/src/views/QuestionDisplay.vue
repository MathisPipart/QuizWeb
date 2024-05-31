<script>
export default {
  props: {
      currentQuestion: {
          type: Object,
          required: true
      }
  },
  methods: {
      handleOptionClick(option) {
          this.$emit('click-on-answer', option);
      }
  }
}
</script>

<style>
.question-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
}
</style>

<template>
  <div class="question-display">
      <h2>{{ currentQuestion.text }}</h2>
      <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" class="question-image">
      <ul>
          <li v-for="option in currentQuestion.options" :key="option" @click="handleOptionClick(option)">
              {{ option }}
          </li>
      </ul>
  </div>
</template>