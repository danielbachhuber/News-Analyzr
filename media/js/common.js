jQuery(document).ready(function(){

	jQuery('.widget span.edit').click(function(){
		jQuery(this).hide();
		jQuery(this).siblings('ul').hide();
		jQuery(this).siblings('form.edit').show();
	});
	
	jQuery('.widget span.cancel').click(function(){
		jQuery(this).parents('form').hide();
		jQuery(this).parents('form').siblings('ul').show();
		jQuery(this).parents('form').siblings('span.edit').show();		
	});
	
	jQuery('.widget form.edit').submit(function(){
        jQuery.post({
            url: jQuery(this).attr('action'),
            data: jQuery(this),
            success: function(data) {
                alert(data.homepage);
            },
        });
		return false;
	});
	
});