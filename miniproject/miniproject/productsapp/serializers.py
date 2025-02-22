from rest_framework import serializers

from .models import Category, Product, ProductImage, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'alt_text', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'category', 'category_name', 'tags', 'stock',
            'is_active', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'category', 'category_name', 'tags', 'tag_ids',
            'stock', 'is_active', 'images', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        tag_ids = validated_data.pop('tag_ids', [])

        product = Product.objects.create(**validated_data)
        if tag_ids:
            product.tags.set(tag_ids)
        for i, image_data in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=image_data,
                is_primary=(i == 0)  # First image is primary
            )

        return product

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        tag_ids = validated_data.pop('tag_ids', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids:
            instance.tags.set(tag_ids)

        if images:
            instance.images.update(is_primary=False)
            for i, image_data in enumerate(images):
                ProductImage.objects.create(
                    product=instance,
                    image=image_data,
                    is_primary=(i == 0)
                )

        return instance
