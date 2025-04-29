function validarNumero(numero) {
    numero = numero.replace(/\D/g, '');
    const regex = /^(?:[1-9][1-9])9[6-9]\d{3}\d{4}$/;
    if (numero && regex.test(numero)) {
      return true;
    } else {
      return false;
    }
}

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email && regex.test(email)) {
      return true;
    } else {
      return false;
    }
}

function validarNome(nome) {
    const regex = /^[A-Za-zÀ-ÖØ-öø-ÿ'’ \-]+(?: [A-Za-zÀ-ÖØ-öø-ÿ'’\-]+)*$/;
    if (nome && regex.test(nome)) {
      return true;
    } else {
      return false;
    }
}

function inputNumero(numero) {
  let value = numero.value.replace(/\D/g, '');
  if (value.length > 11) value = value.slice(0, 11);

  const regex = /^(\d{2})(\d{5})(\d{4})$/;
  if (value.length === 11) {
    numero.value = value.replace(regex, '($1) $2-$3');
  } else if (value.length > 6) {
    numero.value = value.replace(/^(\d{2})(\d{5})/, '($1) $2-');
  } else if (value.length > 2) {
    numero.value = value.replace(/^(\d{2})/, '($1) ');
  } else {
    numero.value = value;
  }
}

function inputEmail(email) {
  email.value = email.value.replace(/[^a-zA-Z0-9@._-]/g, '');

}

function inputNome(nome) {
  nome.value = nome.value.replace(/[^a-zA-ZÀ-ÖØ-öø-ÿ\s]/g, '');
}

async function createUser(data) {
  const myApi = window.location.origin + "/api/" + "client"
  const secondModal = document.getElementById('secondModal');
  const thirdModal = document.getElementById('thirdModal');
      
  const email = document.getElementById("email")
  const telefone = document.getElementById("telefone")
  const btnsbt = document.getElementById("cadastro")

  const error_t = document.getElementById("error-telefone")
  const error_u = document.getElementById("error-undefined")
  const error_e = document.getElementById("error-email")

  try {
    const response = await fetch(myApi, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      if (response.status === 400) {
        const errorResponse = await response.json();
        if (errorResponse.message === "Invalid e-mail") {
          error_e.classList.remove("d-none")
          email.classList.add("is-invalid")
        } else if (errorResponse.message === "Invalid phone") {
          error_t.classList.remove("d-none")
          telefone.classList.add("is-invalid")
        }
      } else if (response.status === 410) {
          error_u.innerText = "Você já está cadastrado para receber o convite"
      } else {
        error_u.innerText = "Erro desconhecido, tente novamente mais tarde"
      }
    } else if (response.ok) {
      $(secondModal).modal('show');
      $(thirdModal).modal('hide');
    }
  } catch (error) {
    console.error(error.message);
  }
  btnsbt.removeAttribute("disabled")
}

async function Email(email) {
  const myApi = window.location.origin + "/api/" + "email/" + email;
  
  try {
    const response = await fetch(myApi, {
      method: "GET",
    });

    if (!response.ok) {
      let errorMessage = "API error";
      if (response.status === 403) {
        const errorResponse = await response.json();
        if (errorResponse.message === "Operation not unsuccessful") {
          errorMessage = "Operation not unsuccessful";
        }
      } else if (response.status === 500) {
        const errorResponse = await response.json();
        if (errorResponse.message === "Invalid e-mail") {
          errorMessage = "Invalid e-mail";
        } else {
          errorMessage = "API error";
        }
      }
      throw new Error(errorMessage);
    }
    return await response.json();
  } catch (error) {
    console.error(error.message);
    throw error;
  }
}



document.addEventListener("DOMContentLoaded", (event) => {
  const btnsbt = document.getElementById("cadastro")
  const nome = document.getElementById("nome")
  const email = document.getElementById("email")
  const telefone = document.getElementById("telefone")
  
  const error_t = document.getElementById("error-telefone")
  const error_n = document.getElementById("error-nome")
  const error_e = document.getElementById("error-email")

  const btnrsd = document.getElementById("reenviar")

  btnrsd.addEventListener("click", function(e) {
    e.preventDefault();
    Email(email.value)
  })

  btnsbt.addEventListener("click", function(e) {
    if (!validarEmail(email.value)) {
      error_e.classList.remove("d-none")
      email.classList.add("is-invalid")
      e.preventDefault();
    } else if (!validarNome(nome.value)) {
      error_n.classList.remove("d-none")
      nome.classList.add("is-invalid")
      e.preventDefault();
    } else if (!validarNumero(telefone.value)) {
      error_t.classList.remove("d-none")
      telefone.classList.add("is-invalid")
      e.preventDefault();
    } else {
      btnsbt.setAttribute("disabled", true)
      createUser({"nome": nome.value, "email": email.value, "telefone": telefone.value})
    }
  })

  nome.addEventListener("click", () => {
    if (!error_n.classList.contains("d-none")) {
      error_n.classList.add("d-none")
    }
    if (nome.classList.contains("is-invalid")) {
      nome.classList.remove("is-invalid")
    }
  })

  email.addEventListener("click", () => {
    if (!error_e.classList.contains("d-none")) {
      error_e.classList.add("d-none")
    }
    if (email.classList.contains("is-invalid")) {
      email.classList.remove("is-invalid")
    }
  })

  telefone.addEventListener("click", () => {
    if (!error_t.classList.contains("d-none")) {
      error_t.classList.add("d-none")
    }
    if (telefone.classList.contains("is-invalid")) {
      telefone.classList.remove("is-invalid")
    }
  })

})
