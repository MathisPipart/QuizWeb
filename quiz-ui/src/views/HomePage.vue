<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";



//const registeredScores = ref([]);

const registeredScores = ref([
  { playerName: "John", score: 10 },
  { playerName: "Jane", score: 20 },
]);

onMounted(async () => { // Au demarrage de la page
  console.log("Home page mounted");

  const scores = await quizApiService.getScores();  // Les erreurs consoles viennent de la car on a pas encore le backend
  registeredScores.value = scores.data;  // Les erreurs consoles viennent de la car on a pas encore le backend
});
</script>

<template>
  <h1>Home page</h1>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <br>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>