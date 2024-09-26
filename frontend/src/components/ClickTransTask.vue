<script>
export default {
    name: 'ClickTransTask',
    props: ['msg'],
    data(){
        return{
            text: '',
            price_netto: '',
            vats: [19, 21, 23, 25],
            selectedVat: 'disabled',
            validationMessage: '',
            hiddenForm: false,
            api_url: import.meta.env.VITE_APP_API_URL,
            is_price_netto_valid: false
        }
    },
    computed: {
        descriptionTextArea() {
            if(this.text.length === 0){
                return "Text is required";
            }
            if(this.text.length === 255){
                return "You can't enter more than 255 characters";
            }
            return `You have ${255 - this.text.length} characters left`;
        },
        priceBrutto(){
            var price = this.price_netto.replace(',', '.');
            if(price !== '' && this.is_price_netto_valid){
                var mod = this.selectedVat / 100 + 1;
                return price * mod;
            }
        },
    },
    methods: {
        async handleSubmit() {
            const apiurl = `${this.api_url}/api/clicktransform/`;
            try {
                const response = await fetch(apiurl);
                if (response.ok) {
                    const data = await response.json();
                    this.hiddenForm = true;
                } else {
                    const errorMessage = await response.text();
                    console.error('Error:', `Error: ${response.status} - ${errorMessage}`); // Log error to console for debugging
                    //alert(`Error: ${response.status} - ${errorMessage}`);
                }
            } catch (error) {
                console.error('Fetch error:', error); // Log error to console for debugging
                //alert(`Network error: ${error.message}`);
            }
        },
        isPriceInputDisabled(){
            return this.selectedVat === 'disabled';
        },
        validateInput() {
            const regex = /^\d*([.,]?\d+)?$/; // Regex for valid float number
            var cond = this.price_netto && !regex.test(this.price_netto);
            this.is_price_netto_valid = !cond;
            this.validationMessage = cond ? 'Please, input number' : '';
        },
    },
};
</script>
<template>
    <form @submit.prevent="handleSubmit" :hidden="hiddenForm">
        <label for="floatingTextarea">Description</label>
        <div class="form-floating">
            <textarea 
                class="form-control"
                placeholder="Leave a comment here"
                id="floatingTextarea"
                v-model="text"
                maxlength="255"
                cols="50"
                required>
            </textarea>
          <label for="floatingTextarea">{{descriptionTextArea}}.</label>
        </div>
        <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="send_confirmation" required>
            <label class="form-check-label" for="send_confirmation">Send confirmation</label>
        </div>
        <div class="mb-3">
            <label for="vat_select" class="form-label">Choose VAT</label>
            <select id="vat_select" class="form-select" v-model="selectedVat" required>
                <option v-for="vat in vats" :value="vat">
                    {{ vat }}%
                </option>
            </select>
        </div>
        <div class="mb-3">
            <label for="price_netto_eur" class="form-label">Price netto EUR</label>
            <input class="form-control" id="price_netto_eur" v-model="price_netto" @input="validateInput" :disabled="isPriceInputDisabled()" required>
            <span v-if="validationMessage" class="error">{{ validationMessage }}</span>
        </div>
        <div class="mb-3">
            <label for="price_brutto_eur" class="form-label">Price brutto EUR</label>
            <input class="form-control" id="price_brutto_eur" :value="priceBrutto" disabled>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <p v-if="hiddenForm" style="padding: 10px; border: 2px solid green; fill: green;">Congratulations!</p>
  </template>

<style scoped>

</style>
