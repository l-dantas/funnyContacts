// Script para aumentar e dinumuir o label dos inputs das telas de login e create pass
$('input[type="password"]').focus((e) => {
	$('label[for='+e.target.id+']').css({
		'top':'10px',
		'font-size':'10px'
	});
}).focusout((e) => {
	if(e.target.value){
		return;
	}
	$('label[for='+e.target.id+']').css({
		top:'40px',
		fontSize:'14px',
	});
});

// desabilitando o autocomplete de todos os input
$('input').attr('autocomplete','off');



$('.btn-sort').click(() => {
	$('.links-sort').toggle();
});

//Ordenando por A-Z - EM DESENVOLVIMENTO
$('.sort-AZ').click(() => {

	console.dir($('.contact'));

	console.dir($('.contact').eq(0).hide());

});


// Sistema de busca
$('.search-contact').keyup(() => {
	let tag_search = $('.search-contact').val();
	console.log(tag_search.length);
	
	if(tag_search.length === 0) {
		$('.contact').show();
	} else {
		$('.contact').hide();
	}

	$('.contact').each(); //aqui vai a buscar pelo contato com o inicio do tag_search

});





// components dos contatos - EM DESENVOLVIMENTO
$('.contact main').hide('slow');
$('.contact').hover((e) => {
	$('.contact main').show();
}, () => {
	$('.contact main').hide(2000,);
});

