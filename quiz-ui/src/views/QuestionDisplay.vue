<script setup>
import { defineProps, defineEmits } from 'vue';

// Reçoit de QuestionsManager
const props = defineProps({
  currentQuestion: Object
});

// Emets vers QuestionsManager
const emit = defineEmits(['click-on-answer']);

const emitAnswer = (answer) => {
  emit('click-on-answer', answer);
};

</script>

<template>
  <div v-if="currentQuestion">
    <h2>{{ currentQuestion.text }}</h2>
    <ul>
      <li v-for="option in currentQuestion.options" :key="option" @click="emitAnswer(option)">
        {{ option }}
      </li>
    </ul>
  </div>
</template>
