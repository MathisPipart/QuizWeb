<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";



//const registeredScores = ref([]);

const registeredScores = ref([
  { playerName: "John", score: 10 },
  { playerName: "Jane", score: 20 },
  { playerName: "Paul", score: 30 },
]);

onMounted(async () => { // Au demarrage de la page
  console.log("Home page mounted");

  const scores = await quizApiService.getScores();  // Les erreurs consoles viennent de la car on a pas encore le backend
  registeredScores.value = scores.data;  // Les erreurs consoles viennent de la car on a pas encore le backend
});
</script>

<template>
  <h1>Home page</h1>
  <br>
  <h2>Classement</h2>
  <div class="scoreboard">
    <div
      v-for="(scoreEntry, index) in registeredScores"
      :key="scoreEntry.playerName"
      :class="{
        first: index === 0,
        second: index === 1,
        third: index === 2,
        other: index >= 3
      }"
    >
      <span class="position">{{ index + 1 }}</span>
      <span class="name">{{ scoreEntry.playerName }}</span>
      <span class="score">{{ scoreEntry.score }}</span>
    </div>
  </div>
  <br>
  <router-link to="/new-quiz" class="start-quiz-link">Démarrer le quiz !</router-link>
</template>

<style scoped>
.start-quiz-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #41b883;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  text-align: center;
  transition: background-color 0.3s;
}

.start-quiz-link:hover {
  background-color: #3a9d70;
}
</style>


<style src="../css/Scores.css"></style>