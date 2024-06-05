<template>
  <div class="question-display">
    <h2>{{ currentQuestion.text }}</h2>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" class="question-image">
    <div class="options-container">
      <div
        class="question-option"
        v-for="(option, index) in currentQuestion.options"
        :key="index"
        @click="handleOptionClick(index)"
        :class="{
          correct: selectedOption === index && option === currentQuestion.correctAnswer,
          incorrect: selectedOption === index && option !== currentQuestion.correctAnswer
        }"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    currentQuestion: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedOption: null
    };
  },
  methods: {
    handleOptionClick(index) {
      if (this.selectedOption === null) {
        this.selectedOption = index;
        this.$emit('click-on-answer', index);
      }
    }
  },
  watch: {
    currentQuestion() {
      this.selectedOption = null;
    }
  }
}
</script>

<style scoped>
.question-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
}

.options-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  max-width: 100%;
}

.question-option {
  cursor: pointer;
  padding: 1rem;
  background-color: #2e62af;
  border-radius: 5px;
  transition: background-color 0.3s;
  text-align: center;
}

.question-option:hover {
  background-color: rgba(46, 98, 175, 0.56);
}

.question-option.correct {
  background-color: #28a745;
}

.question-option.incorrect {
  background-color: #dc3545;
}
</style>
