<script>
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      username: ''
    }
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    launchNewQuiz() {
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName(this.username);
      const playerName = participationStorageService.getPlayerName();
      this.router.push('/questions');
    }
  }
}
</script>

<template>
  <div class="new-quiz">
    <h1>Nouvelle page de quiz</h1>
    <br>
    <p>Saisissez votre nom :</p>
    <input type="text" v-model="username" placeholder="Username" class="form-control" />
    <button type="submit" class="btn btn-success mt-2" @click="launchNewQuiz">GO!</button>
  </div>
</template>
