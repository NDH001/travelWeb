from django.db.models import Max, Min
from django.contrib.auth.hashers import make_password
import random
import json
import os
import time
from os import listdir
from os.path import isfile, join

from django.contrib.auth.models import User
from journing.models import Comment
from traveldata.models import Sights, Cities
from userdata.models import Connection

random_text = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum interdum erat vel leo euismod, non accumsan justo varius. Vestibulum at erat tellus. Integer dignissim sapien eros, sit amet semper erat hendrerit et. Quisque eget eros malesuada, cursus lacus quis, hendrerit arcu. Morbi ultrices sapien mi, dictum auctor augue placerat sed. Aliquam fringilla convallis ligula vel efficitur. In eros justo, iaculis eu leo quis, hendrerit laoreet sapien. Suspendisse potenti. In sed tortor a dui hendrerit placerat quis a nibh. Nulla sed euismod eros, id convallis orci. Aliquam pretium purus non eros pulvinar volutpat. Proin vehicula aliquet turpis nec eleifend.",
    "In eget ultrices ipsum. Vestibulum dui tellus, lobortis quis dictum eget, elementum sed lacus. Sed dapibus magna nunc, ornare ornare est lacinia semper. Cras a malesuada sem. Proin id justo vel diam condimentum bibendum. Proin eget condimentum ex. Proin facilisis pulvinar mauris non lacinia. Vivamus velit sapien, faucibus at odio ut, accumsan elementum odio. In bibendum urna eros, nec placerat dui aliquam quis. Suspendisse potenti.",
    "Morbi efficitur odio a nibh tristique molestie id id ante. In hac habitasse platea dictumst. Morbi vitae ex id eros suscipit luctus vel eget neque. Etiam interdum ut nunc in sodales. Proin accumsan, mauris vitae fringilla rhoncus, enim lectus interdum lorem, in rutrum neque turpis sed lorem. Duis molestie, sem ac efficitur tempus, nulla nisi rutrum sem, sit amet ullamcorper eros arcu vel lorem. Nam ullamcorper libero nibh, vel malesuada elit porttitor sit amet. Proin dolor massa, vestibulum pretium risus eget, semper venenatis purus. Maecenas nibh eros, congue sit amet interdum at, porttitor interdum dolor. Mauris sit amet mollis nibh. Morbi ac ex eget sapien gravida faucibus. Morbi pharetra metus at lacus interdum, ac vestibulum dolor venenatis. Fusce sodales lacus lacinia, mollis magna nec, porta ex. Aenean ut purus fermentum sapien pulvinar pretium vitae eget risus. Vivamus non ligula maximus, scelerisque leo eget, aliquam quam. Nulla vitae placerat purus. Cras nisi metus, ultricies id eros nec, ornare vestibulum ligula. Donec ipsum leo, accumsan ac cursus vitae, lacinia id metus. Praesent eget malesuada quam. Curabitur eros felis, elementum ut sem nec, blandit consectetur diam.",
    "Quisque vel eros sit amet elit euismod laoreet. Praesent id dapibus ipsum. Sed aliquam dolor sed justo mattis congue. Duis eu interdum nulla, id posuere nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean venenatis dignissim ex quis pharetra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut nisl varius, vehicula nisi sit amet, venenatis erat. Praesent ultricies quam sed mauris hendrerit, id interdum arcu convallis.",
    "Mauris urna lorem, maximus a mi at, tempus euismod ex. Pellentesque sem urna, congue vitae justo sit amet, bibendum elementum urna. Duis pretium libero quis arcu dapibus, nec elementum est luctus. Aliquam quis turpis rhoncus, faucibus est eu, imperdiet sapien. Vestibulum facilisis, dolor non porttitor imperdiet, purus augue eleifend metus, vitae tempus lacus arcu cursus mauris. Pellentesque a iaculis massa. Vivamus eget dolor turpis. Maecenas ut facilisis odio. Vivamus ut lectus vitae nibh maximus sodales. Maecenas et fringilla mi, nec tristique sem. Nunc eget fringilla sem. Mauris rhoncus ut magna sed ultricies. Quisque quis vulputate ligula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam volutpat et diam quis rhoncus. Fusce pretium, odio eu gravida iaculis, lectus erat dictum sapien, eget mollis ante justo rutrum nibh. Duis vitae eleifend erat. Morbi purus dui, suscipit sit amet ligula sed, convallis varius diam. Suspendisse a vestibulum odio. Maecenas euismod finibus neque eget convallis. Sed id ipsum ultricies, pellentesque nibh eu, mattis velit. Vestibulum accumsan lectus accumsan velit ornare sollicitudin. Praesent venenatis suscipit ex, sed viverra purus imperdiet sit amet. Quisque imperdiet quis diam sed ultricies.",
    "Aliquam et orci eleifend, pretium erat nec, rhoncus arcu. Sed massa metus, pulvinar sit amet egestas commodo, auctor eget risus. Morbi eu dui eu purus eleifend tristique. Pellentesque ullamcorper neque eu interdum egestas. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas sollicitudin, justo sed pretium malesuada, mi risus viverra tellus, sed molestie enim quam id erat. Cras imperdiet bibendum turpis, sit amet vestibulum elit auctor vestibulum. Suspendisse libero neque, pharetra sit amet mauris auctor, sollicitudin bibendum est. Mauris massa enim, posuere vitae metus eget, porttitor sagittis est. Suspendisse blandit nisi quis ornare fermentum. Nulla tempus euismod lectus. Nulla condimentum felis nec tellus tincidunt imperdiet.",
    "Nullam commodo pulvinar neque id condimentum. Praesent et pulvinar purus. Aenean nec massa bibendum, ornare mauris ac, cursus lectus. Aenean aliquet lectus nec felis tempus, ut tempor elit sodales. Donec semper mauris ac sapien porttitor, mollis pellentesque justo luctus. In tristique lectus erat, vitae fermentum ex imperdiet porttitor. Proin egestas ultricies risus et malesuada. Aenean a orci a tortor fermentum elementum et vitae nisl. Nam venenatis urna est, ut ullamcorper nunc feugiat sed. Morbi iaculis viverra dictum. Nullam efficitur, sapien ut finibus tincidunt, dui orci iaculis nisl, non pharetra elit turpis in ligula. Cras vitae tempor magna, ut vehicula urna. Vivamus massa nisi, porttitor eget dignissim eget, pulvinar eu tortor. Nullam sit amet augue sed leo vestibulum suscipit.",
    "Vivamus a ultricies diam. Nam fermentum felis id eros maximus, in accumsan sapien lobortis. Aliquam et risus vulputate, facilisis nisi at, commodo tellus. Quisque a elit at felis maximus gravida et et ante. Maecenas at finibus ipsum, a rutrum quam. Duis tempus metus vel elit cursus cursus. Sed sit amet elementum augue, non condimentum felis.",
    "Ut eu tempus diam. Phasellus malesuada odio id tellus hendrerit semper. Duis ullamcorper ultricies lacus facilisis blandit. Nunc id arcu ultricies, eleifend sapien eget, mollis diam. Pellentesque imperdiet erat sed neque suscipit lacinia. Nullam nec lorem dapibus, volutpat dui eget, aliquam ex. Nam et purus massa. Nullam sed pellentesque neque. Ut pellentesque tempus nisl ac efficitur.",
    "Sed vitae elementum ante. Sed tincidunt, urna at venenatis convallis, purus metus hendrerit massa, quis rutrum quam ligula ac nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur malesuada erat id diam volutpat ullamcorper vitae non tortor. Vestibulum commodo tristique diam et rhoncus. Ut tincidunt magna euismod augue rutrum consectetur. Integer convallis ultrices dui, quis interdum elit ultrices at. Sed dictum nunc augue. Donec ut orci dolor.",
    "In congue porta dolor, fringilla vehicula purus lacinia ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec sagittis vestibulum erat, in euismod urna tincidunt eget. Quisque dui ante, finibus non risus quis, scelerisque vestibulum risus. Suspendisse sagittis semper semper. Curabitur a ipsum quis dolor tristique tincidunt. Etiam varius mattis tristique. Phasellus vel nulla a libero mollis feugiat. Aliquam ut facilisis magna, quis porta lectus. Mauris rhoncus ultrices neque, quis auctor tellus euismod nec. Aliquam vel enim cursus, viverra libero non, feugiat mi. Quisque sed lacus ex. Etiam eu ex vitae felis viverra condimentum nec sit amet nisi. Etiam a efficitur turpis.",
    "Maecenas consectetur, felis varius condimentum pulvinar, quam lacus accumsan nulla, vel posuere quam nibh in ex. Aenean laoreet metus non congue egestas. Curabitur molestie consectetur nibh vitae ornare. Quisque et sapien vel libero gravida consequat. Quisque dapibus, quam nec imperdiet accumsan, odio tellus fermentum est, eu elementum lectus tortor nec odio. Ut varius neque ut feugiat maximus. Vestibulum ultricies convallis quam et fringilla. Proin tristique purus in pretium lobortis. Sed varius eu dui et convallis. In ut erat eget quam imperdiet elementum. Fusce elementum convallis accumsan. \n In in mauris auctor lacus semper pretium. Duis a odio tortor. Nam vestibulum mattis auctor. Curabitur in eros non nisi blandit vulputate at vel risus. Integer eget congue tortor. Cras sed ligula eros. Phasellus porttitor, quam in vehicula euismod, felis lorem fringilla neque, vitae pretium erat orci in felis. Maecenas volutpat a massa id mattis. Ut ullamcorper lorem sit amet aliquet tempor. Etiam sit amet sapien in augue ornare imperdiet id sed felis. Vivamus volutpat sagittis posuere. Vestibulum nec iaculis justo, ac fermentum augue. Maecenas condimentum tempus nulla non consectetur. Suspendisse eget dolor vehicula, tristique mauris volutpat, condimentum sem.",
    "Ut consectetur tincidunt varius. Curabitur vitae nulla quam. In eu mauris at leo fringilla rhoncus. Quisque malesuada mi a vehicula fermentum. Praesent laoreet sem in arcu sagittis euismod. Aenean luctus eros purus, id scelerisque purus euismod eget. Praesent enim magna, finibus vel arcu a, efficitur tempus massa. Nulla felis neque, rhoncus nec nunc non, rhoncus ornare nulla. Vestibulum sit amet neque vel enim sagittis pulvinar.",
    "Praesent vel augue eros. In hac habitasse platea dictumst. Praesent sagittis, magna faucibus semper cursus, velit felis dignissim nibh, sit amet pulvinar lectus leo eget sem. Ut ultricies consectetur lectus a imperdiet. In placerat metus et pellentesque faucibus. Etiam et facilisis metus, sit amet maximus ante. Sed mollis felis sit amet felis pellentesque hendrerit. Sed rutrum imperdiet est, quis fermentum lorem hendrerit in. Etiam eleifend magna eget tortor maximus, ac semper nulla ullamcorper. Aenean ut velit a augue commodo ultricies non sed elit.",
    "Nam congue tempus ante, id consequat tellus tincidunt non. In eget turpis lectus. Fusce id accumsan ipsum. Maecenas bibendum elit id ante suscipit molestie. Praesent non euismod lacus, sed sodales purus. Morbi urna felis, pulvinar et sem tristique, blandit sagittis risus. Suspendisse ultrices finibus purus, id cursus dui laoreet at. Fusce id neque accumsan, posuere purus vitae, pulvinar enim. Pellentesque sapien massa, maximus vitae sapien in, feugiat placerat massa. Praesent ante tortor, cursus quis vestibulum ut, lobortis et ante. Praesent vel euismod neque, vel pretium elit. Cras placerat tortor mattis eleifend cursus. Maecenas aliquam ornare mi, nec condimentum ex pulvinar nec. Nunc ac urna lectus. Sed lacinia euismod odio, eu lobortis est varius sit amet.\n Vestibulum suscipit sodales enim eu mattis. Quisque non erat magna. In aliquam quam tellus, in iaculis dolor tempor sagittis. Curabitur varius, nisi in luctus venenatis, augue lacus placerat dolor, id accumsan nisi eros ac tellus. Suspendisse sed orci vitae turpis pharetra eleifend. Etiam elementum purus at purus scelerisque auctor. Curabitur porttitor ornare metus a ornare. Integer in elit laoreet arcu molestie posuere condimentum id elit. Donec leo dolor, sodales eu faucibus non, gravida non purus. \n Fusce vehicula euismod arcu sit amet imperdiet. Sed sit amet laoreet libero. Vestibulum imperdiet luctus laoreet. Sed sed neque eget purus laoreet posuere. Aliquam consequat neque at metus consectetur, nec iaculis magna dictum. Vivamus at molestie lectus. Maecenas accumsan nec sem sit amet facilisis.",
    "Nulla sed ligula ac massa accumsan finibus id non mi. Aliquam iaculis sem ipsum, id pharetra dolor tempus non. Etiam ultricies lobortis eros, quis eleifend magna vestibulum at. Sed hendrerit consectetur leo, ut bibendum augue interdum sed. Etiam a porttitor orci, in finibus risus. Duis semper justo et rhoncus finibus. In at justo nec est ornare venenatis in et velit.",
    "Nam molestie consequat quam vitae mollis. Donec nec dapibus nunc. Vestibulum dignissim quam odio, id feugiat metus feugiat quis. Maecenas efficitur ut libero quis vehicula. Duis vel justo in leo fringilla lobortis eu vestibulum neque. Nam condimentum dictum orci sit amet faucibus.al",
    "Curabitur rutrum finibus libero, vel malesuada purus pellentesque non. Curabitur ante eros, mollis quis consectetur at, dapibus congue mi. Donec eget vestibulum leo. ",
    "Proin at quam odio. Phasellus eu orci pharetra, ultricies libero sed, posuere leo. Nullam et aliquam purus, vitae aliquam mi. Nunc auctor ligula eget magna efficitur rhoncus. Nulla commodo ac augue at dignissim. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla est arcu, tincidunt sit amet rutrum hendrerit, aliquet vitae enim. Proin magna odio, tristique sit amet eros et, scelerisque maximus dui. Praesent rhoncus neque quis quam tincidunt, ac tempor turpis varius. Duis volutpat elit quis eros vulputate, hendrerit tempor nibh cursus. Donec vitae purus accumsan, commodo nulla sed, venenatis purus. Mauris gravida tincidunt mauris vitae lacinia. Cras id lorem erat.",
    "Nullam fringilla porttitor placerat. Vivamus consequat diam vitae pellentesque consequat. Aenean pellentesque, nisi in interdum maximus, lorem mauris consequat orci, in aliquet eros urna quis urna. Fusce molestie, dolor eget rutrum venenatis, orci enim eleifend sem, quis mollis arcu diam in felis. Aliquam et nulla et sem convallis bibendum. Vivamus ut elit pulvinar, suscipit justo in, consequat neque. Phasellus a quam erat. Etiam a ultricies purus. Duis massa est, venenatis at tellus vel, tempus sollicitudin sem.",
    "Vivamus imperdiet elit congue, vehicula diam at, fringilla magna. Donec at ligula blandit, sodales orci quis, ornare orci. Pellentesque ornare eros a ipsum ultricies iaculis. Curabitur vel aliquet elit, sed porta dolor. Morbi blandit auctor risus, sit amet molestie massa porta in. Etiam eleifend nibh malesuada, tempus sem quis, aliquam lorem. In hac habitasse platea dictumst. Sed porttitor arcu ac sem ultrices, in tempus mi dictum. Fusce vitae elementum neque. Aenean commodo ex ac orci ornare ornare. Nullam in rhoncus dui, non faucibus ligula. In iaculis elementum nisi. Fusce at magna pharetra, lacinia turpis vel, fermentum nulla. Aenean faucibus purus nulla, ac commodo urna condimentum non.",
    "Nullam fringilla porttitor placerat. Vivamus consequat diam vitae pellentesque consequat.",
    "Aenean pellentesque, nisi in interdum maximus, lorem mauris consequat orci, in aliquet eros urna quis urna. Fusce molestie, dolor eget rutrum venenatis, orci enim eleifend sem, quis mollis arcu diam in felis.",
    "Aliquam et nulla et sem convallis bibendum. Vivamus ut elit pulvinar, suscipit justo in, consequat neque. Phasellus a quam erat. Etiam a ultricies purus. Duis massa est, venenatis at tellus vel, tempus sollicitudin sem.",
    "In sit amet fermentum ante.",
    "Fusce erat tortor, ullamcorper et est non, vulputate convallis metus.",
    "Morbi euismod ipsum malesuada commodo congue.",
    "Nullam in mi metus.",
    "Donec in lacinia felis. Etiam eu maximus velit. Sed ornare mattis tristique. Phasellus at sapien nisi. ",
    "Quisque feugiat lacus imperdiet semper dictum. Praesent mi arcu, vulputate in augue vitae, volutpat fringilla magna. Ut feugiat quam in purus suscipit sollicitudin. Vivamus sollicitudin luctus justo eget ultrices. Quisque porta, ipsum a suscipit pellentesque, turpis metus suscipit dolor, at dapibus mi justo malesuada ante",
    "Vestibulum non sapien suscipit, fermentum ipsum vitae, ullamcorper tortor. Curabitur quis leo vel risus consectetur rhoncus eleifend at nisl. Morbi vitae ultricies sapien. Proin dictum diam ex, eget sodales lectus vestibulum et. Fusce vehicula, ligula in feugiat malesuada, enim est porta neque, et aliquet velit ipsum sit amet nibh. Aenean in ipsum placerat, venenatis nulla eleifend, lacinia nisi. Vivamus luctus lacus urna. Nulla tincidunt scelerisque justo. In lacinia id diam sit amet porta. Proin semper, quam vel dictum mattis, nibh sapien mattis risus, ac finibus ligula justo quis erat. Suspendisse porttitor tempor volutpat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas suscipit gravida orci sit amet sollicitudin. Donec dictum mi sed mauris iaculis eleifend.",
    "Nullam enim sem, volutpat nec erat sagittis, rhoncus efficitur est. Vivamus eu tellus elit. Phasellus in cursus leo, ut vehicula diam. Donec sit amet tempor diam. In lacinia libero et ex bibendum, quis semper orci sagittis. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla et sem at felis rutrum viverra.",
    "Quisque pellentesque mauris sem, ac sodales erat fermentum id. Mauris porta est a finibus posuere. Fusce condimentum id turpis id consequat. Aenean placerat sem sit amet mi rutrum, non sodales mi vestibulum. Donec feugiat in ante sit amet placerat. Suspendisse euismod lorem eget dolor convallis, eu porttitor est imperdiet. Proin quis nisi efficitur, tristique mauris in, finibus lectus. Nulla varius porta sem ut maximus. In a tellus sapien. Nulla hendrerit, leo non ultricies semper, nulla tellus feugiat nunc, eu dapibus nisi arcu sed purus. Nullam pretium ullamcorper finibus.",
    "Aenean et lorem consectetur, feugiat urna ac, interdum sapien. Morbi fermentum odio quis ullamcorper dapibus. Sed nulla nisl, pharetra rutrum ligula quis, tristique imperdiet elit. Curabitur vulputate nec ante quis cursus. Vivamus convallis convallis fringilla. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut at metus id lacus posuere mattis. In et urna nunc. Praesent est enim, feugiat sit amet ipsum porttitor, venenatis semper dui. Maecenas pulvinar urna eu dictum volutpat. Etiam porttitor facilisis sagittis. Nullam eget augue et nunc sagittis pharetra. Sed ac nibh eu tortor mattis blandit. Curabitur rutrum pellentesque augue, id maximus enim laoreet ac. Nulla sed turpis massa. Curabitur aliquam laoreet eros, sed euismod nunc vulputate vitae.",
    "Nulla quis diam nibh.",
    "Donec dolor nibh, hendrerit id erat non, sagittis egestas nunc. Quisque bibendum sed dolor et rhoncus. In non facilisis quam. ",
    "Nunc euismod ac nunc sed dignissim. Ut ut vulputate dui. Suspendisse potenti. Donec malesuada dui commodo arcu lacinia, in volutpat mi maximus. Suspendisse rutrum ipsum quis augue pellentesque porttitor. Vestibulum tincidunt velit ac leo mattis, nec mattis sem eleifend. Pellentesque eget feugiat massa. ",
]

path = os.getcwd() + "/media/profile_pics"
images = [f for f in listdir(path) if isfile(join(path, f))]


def get_userid_min_max():
    min_id = User.objects.aggregate(min_id=Min("id"))["min_id"]
    max_id = User.objects.aggregate(max_id=Max("id"))["max_id"]

    return min_id, max_id


def create_users():
    imgs_len = len(images)

    another_account = User.objects.create(
        username="jun000111",
        email="zhijun950@gmail.com",
        password=make_password("forwhat000"),
    )
    another_account.save()

    # another_account = User.objects.create(
    #     username="jun000222",
    #     email="zhijun952@gmail.com",
    #     password=make_password("forwhat000"),
    # )
    # another_account.save()

    # another_account = User.objects.create(
    #     username="jun000333",
    #     email="zhijun953@gmail.com",
    #     password=make_password("forwhat000"),
    # )
    # another_account.save()

    # another_account = User.objects.create(
    #     username="jun000444",
    #     email="zhijun954@gmail.com",
    #     password=make_password("forwhat000"),
    # )
    # another_account.save()

    with open("users.json") as f:
        new_users = json.load(f)

    for i, new_user in enumerate(new_users):
        print(i)
        print(new_user["name"], new_user["email"], new_user["password"])
        user = User.objects.create(
            username=new_user["name"],
            email=new_user["email"],
            password=make_password(new_user["password"]),
        )
        gender = random.randint(0, 1)
        pic = random.randint(0, imgs_len - 1)
        user.profile.gender = gender
        user.profile.desc = new_user["statement"]
        user.profile.profile_pic = "profile_pics/" + images[pic]
        user.save()


def add_comments():
    users = list(User.objects.all())
    sights = list(Sights.objects.filter(city__in=["上海", "北京", "新加坡"]))

    user_len = len(users)
    sight_len = len(sights)
    text_len = len(random_text)

    for i in range(5000):
        print(i)
        ur = random.randint(0, user_len - 1)
        sr = random.randint(0, sight_len - 1)
        tr = random.randint(0, text_len - 1)
        rating = random.randint(0, 5)
        comment = Comment.objects.create(
            user=users[ur], sight=sights[sr], comment=random_text[tr], rating=rating
        )
        comment.save()


def add_connection():
    min_id, max_id = get_userid_min_max()
    print(min_id, max_id)

    user1 = User.objects.all().select_related("profile")
    user2 = User.objects.all().select_related("profile")

    seen = set()
    count = 0
    for i in range(5000):
        print(i)

        ur = random.randint(0, len(user1) - 1)
        tr = random.randint(0, len(user2) - 1)

        user_2 = user2[ur]
        user_1 = user1[tr]

        if user_2 != user_1 and (user_2, user_1) not in seen:
            count += 1
            seen.add((user_2, user_1))

            connection = Connection.objects.create(user=user_1, follower=user_2)
            connection.save()
            print(connection.id, user_2.id, user_1.id, "new connection")
        else:
            print(user_2.id, user_1.id, "duplicated")

    print(f"total: {count}")


def create_contents():
    create_users()
    add_connection()
    add_comments()
