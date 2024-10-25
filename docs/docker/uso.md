# instalação e uso do contâiner

a aplicação pode ser rodada facilmente através da interface do Docker e do DockerHub. 

## pré-requisitos

para rodar o projeto, você irá precisar de:

- [docker](https://docs.docker.com/engine/install/) e [docker compose](https://docs.docker.com/compose/install/) instalados na sua máquina
- o arquivo `compose.yml`
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (opcional)

## instalação

baixe o arquivo `compose.yml`:

<a href="https://raw.githubusercontent.com/brunozalc/projeto-cloud/main/compose.yml" id="downloadLink">compose.yml</a>

<script>
document.getElementById('downloadLink').addEventListener('click', function(event) {
    event.preventDefault();
    const url = this.href;
    const fileName = 'compose.yml';

    fetch(url)
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
    })
    .catch(() => alert('falha ao baixar o arquivo.'));
});
</script>

ou clone o repositório do projeto no seu computador:

```bash
git clone https://github.com/brunozalc/projeto-cloud.git
```

# uso

abra um terminal ou prompt de comando no mesmo local em que você armazenou o `compose.yml` ou o repositório, e inicie a API:

```bash
docker compose up
```

espere alguns segundos, e a API ficará disponível em `http://localhost:8080`

você pode ver a documentação dos *endpoints* da API em `http://localhost:8080/docs`, além de testá-los interativamente!
