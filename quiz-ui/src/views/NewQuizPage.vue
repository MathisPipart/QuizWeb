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
      // const playerName = participationStorageService.getPlayerName();
      this.router.push('/questions');
    }
  }
}
</script>

<template>
  <div class="new-quiz">
    <h1>Lancement du Quiz</h1>
    <br>
    <div class="BoiteName">
      <p>Saisissez votre nom :</p>
      <input type="text" v-model="username" placeholder="Username" class="form-control" />
      <button type="submit" class="btn btn-success mt-2" @click="launchNewQuiz">GO!</button>
    </div>
  </div>
</template>

<style>
.form-control {
  width: 20%;
  padding: 5px;
  margin-right: 10px;
}

.BoiteName {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 800px;
  max-height: 250px;
  padding: 20px;
  border-radius: 15px;
  padding: 20px;
  margin: 0 auto;
  margin-top: 5%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.BoiteName .form-control {
  text-align: center;
  width: 50%;
}
.BoiteName .form-control:focus {
  border-color: #a5ada1;
  box-shadow: 0 0 5px rgba(144, 164, 143, 0.8);
}
</style>