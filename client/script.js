function KanyeClient() {

  API_ROOT = "http://localhost:8000/api/v1";

  let form = document.getElementById("get_quotes_form");
  form.addEventListener('submit', getAndAnalyzeQuotes);

  async function getAndAnalyzeQuotes(event) {
    event.preventDefault();
    let quote_input = document.getElementById("quote_number");
    // Rely on html validation
    if (quote_input.validity.invalid) {
      return;
    }
    getQuotes(quote_number.value);
  }

  async function getQuotes(quote_number) {
    document.getElementById("quotes").innerHTML =
      "Wating for some Kanye quotes...";
    const url = API_ROOT + "/quotes?number=" + quote_number;
    fetch(url)
      .then(handleResponse)
      .then(renderQuotes)
      .catch(function (error) {
        console.log(error);
        let error_text = "Can't get quotes now. Sorry :(";
        document.getElementById("quotes").innerHTML = error_text;
      });
  }
  async function handleResponse(response) {
    if (response.ok) {
      return response.json();
    }
    throw new Error();
  }

  async function renderQuotes(quotes_json) {
    let quote_list = document.getElementById("quotes");
    quote_list.innerHTML = "";
    for (quote of quotes_json["quotes"]) {
      let quote_li = document.createElement("li");
      let quote_q = document.createElement("q");
      quote_q.innerHTML = quote;
      quote_li.appendChild(quote_q);
      quote_list.appendChild(quote_li);
    }
    return quotes_json["quotes"];
  }

  async function getQuoteAnalysis() {
    pass;
  }
  return {
    getAndAnalyzeQuotes: getAndAnalyzeQuotes,
  };
}

let kanye_client = KanyeClient();
