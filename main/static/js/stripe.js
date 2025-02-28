document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe('pk_test_TYooMQauvdEDq54NiTphI7jx', {
        locale: 'ru'
    });
    
    var buyButton = document.getElementById('buy-button');
    if (buyButton) {
        buyButton.addEventListener('click', function() {
            var objectId = buyButton.getAttribute('data-object-id');
            var obj_type = buyButton.getAttribute('obj_type');
            var currencySelect = document.getElementById('curr');
            var selectedCurrency = currencySelect.value;
            if (obj_type=='order') {
                var url = '/buy-order/'
            }
            else {
                var url = '/buy/'
            }
            fetch(url + objectId + '?currency=' + selectedCurrency, { method: 'GET' })
                .then(response => response.json()) 
                .then(session => {
                    if (session.id) {
                        stripe.redirectToCheckout({ sessionId: session.id });
                    } else {
                        console.error('Session ID not found in response');
                    }
                })
                .catch(error => {
                    console.error('Error:', error); 
                });
        });
    }
    
    // Показать форму оплаты карты при нажатии на кнопку
    var showCardPaymentButton = document.getElementById('show-card-payment');
    var paymentForm = document.getElementById('payment-form');
    
    if (showCardPaymentButton) {
        showCardPaymentButton.addEventListener('click', function() {
            paymentForm.style.display = 'block';
            showCardPaymentButton.style.display = 'none';
            
            // Инициализация элемента карты только после показа формы
            const elements = stripe.elements();
            const cardElement = elements.create('card');
            cardElement.mount('#card-element');
        });
    }
    
});