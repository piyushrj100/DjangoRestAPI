from rest_framework import serializers
from watchlist_app.models import Watchlist, StreamPlatform, Review




class ReviewSerializer(serializers.ModelSerializer) :
    
    class Meta :
        model = Review 
        fields = "__all__" 
class WatchlistSerializer(serializers.ModelSerializer) :
    len_name = serializers.SerializerMethodField() 
    reviews = ReviewSerializer(many=True, read_only =True)
    class Meta :
        model =Watchlist
        fields = "__all__"
        # fields=['id','name','description']
        # exclude=['active']

    def get_len_name(self,object) :
        length=len(object.title)
        return length






class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer) :
    url = serializers.HyperlinkedIdentityField(view_name="stream-detail")
    # watchlist = WatchlistSerializer(many=True, read_only = True)
    watchlist = serializers.StringRelatedField(many=True)  # this will use the model and use the __str__ method to return the field
    #We will be using the hyperlinked related field so that clicking on it will take us to the actual movies. 

    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )

    class Meta :
        model = StreamPlatform
        fields = "__all__"

    # def validate(self,data) :
    #     if data['name'] ==data['description'] :
    #         raise serializers.ValidationError("Title and Description should be different")
    #     else :
    #         return data
    
    # def validate_name(self,value) : 
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     else :
    #         return value





# def name_length(value) :
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")
#     else :
#         return value

# class MovieSerializer(serializers.Serializer) :
#     id  = serializers.IntegerField(read_only= True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField() 

#     def create(self, validated_data) :
#         return Movie.objects.create(**validated_data)
    

#     def update(self, instance,validated_data) :
#         instance.name = validated_data.get('name',instance.name) 
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)  
#         instance.save()
#         return instance
    
    # def validate_name(self,value) : 
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     else :
    #         return value
    
#     def validate(self,data) :
#         if data['name'] ==data['description'] :
#             raise serializers.ValidationError("Title and Description should be different")
#         else :
#             return data 






