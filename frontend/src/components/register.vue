<template>
  <form @submit.prevent="submit">
    <div>
      <label>Username</label>
      <input
        v-model="form.username"
        @input="clearError('username')"
      />
      <p v-if="errors.username" class="error">
        {{ errors.username }}
      </p>
    </div>

    <div>
      <label>Email</label>
      <input
        v-model="form.email"
        @input="clearError('email')"
      />
      <p v-if="errors.email" class="error">
        {{ errors.email }}
      </p>
    </div>

    <div>
      <label>Password</label>
      <input
        type="password"
        v-model="form.password"
        @input="clearError('password')"
      />
      <p v-if="errors.password" class="error">
        {{ errors.password }}
      </p>
    </div>

    <button type="submit">Register</button>
  </form>
</template>

<script setup>
import { reactive } from "vue";

const form = reactive({
  username: "",
  email: "",
  password: ""
});

const errors = reactive({});

function clearError(field) {
  delete errors[field];
}

async function submit() {
  // Clear old errors
  Object.keys(errors).forEach(k => delete errors[k]);

  const res = await fetch("http://localhost:8000/api/v0/user/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form)
  });

  if (res.status === 422) {
    const data = await res.json();

    data.detail.forEach(err => {
      const field = err.loc[1]; // body → field name
      errors[field] = err.msg.replace(/^Value error, /, "");;
    });

    return;
  }

  if (!res.ok) {
    alert("Unexpected error");
    return;
  }

  alert("Registration successful!");
}
</script>

<style scoped>
.error {
  color: red;
  font-size: 0.9em;
}
</style>
