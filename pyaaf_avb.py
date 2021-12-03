import aaf2

# with aaf2.open("Aaf TestSeq.aaf", "r") as f:
with aaf2.open("AAF TestBin1202.avb.aaf", "r") as f:
    print('header = ', f.header)
    
    print('dictionary = ', f.dictionary)
    # for p in f.dictionary.properties():
    #     print('dic = ', p.)



    # get the main composition
    main_compostion = next(f.content.toplevel())

    # print the name of the composition
    print(main_compostion.name)

    # AAFObjects have properties that can be
    # accessed just like a dictionary
    print(main_compostion['CreationTime'].value)

    # video, audio and other track types are
    # stored in slots on a mob object.
    for slot in main_compostion.slots:
        segment = slot.segment
        print(segment.class_id)
    
    mobs = f.content.mobs
    for mob in mobs:
        print('mob name = ', mob.name)
        print('mob id = ', mob.mob_id)

        if str(mob.class_id) == '0d010101-0101-3500-060e-2b3402060101':
            print('mob class id = {0}, mob_type = {1} '.format(mob.class_id, 'composition'))
        elif str(mob.class_id) == '0d010101-0101-3600-060e-2b3402060101':
            print('mob class id = {0}, mob_type = {1} '.format(mob.class_id, 'master'))
        elif str(mob.class_id) == '0d010101-0101-3700-060e-2b3402060101':
            print('mob class id = {0}, mob_type = {1} '.format(mob.class_id, 'source'))
