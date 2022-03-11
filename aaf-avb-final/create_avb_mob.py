import avb

def create_mastermob(f, mob_name, start_time, length):
    edit_rate = 25

    tape_mob =  f.create.Composition(mob_type="SourceMob")
    tape_mob.descriptor = f.create.TapeDescriptor()
    tape_mob.descriptor.mob_kind = 2 # won't work without
    tape_mob.name = mob_name
    tape_mob.length = 10368000

    track = f.create.Track()
    track.index = 1
    track.component = f.create.Timecode(edit_rate=edit_rate, media_kind='timecode')
    track.component.length = 10368000
    tape_mob.tracks.append(track)

    track = f.create.Track()
    track.index = 1
    track.component = f.create.SourceClip(edit_rate=edit_rate, media_kind='picture')
    track.component.length = length
    track.filler_proxy = f.create.TrackRef(edit_rate=edit_rate, media_kind='picture')
    track.filler_proxy.length = 2147483647
    tape_mob.tracks.append(track)

    file_mob = f.create.Composition(mob_type="SourceMob")
    file_mob.descriptor = f.create.CDCIDescriptor()
    file_mob.descriptor.length = length
    file_mob.descriptor.mob_kind = 1 # won't work without
    file_mob.length = length
    track = f.create.Track()

    track.index = 1
    track.component = f.create.SourceClip(edit_rate=edit_rate, media_kind='picture')
    track.component.length = length
    track.component.track_id = 1
    track.component.start_time = start_time
    track.component.mob_id = tape_mob.mob_id
    track.filler_proxy = f.create.TrackRef(edit_rate=edit_rate, media_kind='picture')
    track.filler_proxy.length = 2147483647

    file_mob.tracks.append(track)

    mob = f.create.Composition(mob_type="MasterMob")
    mob.name = mob_name

    track = f.create.Track()
    track.index = 1
    track.filler_proxy = f.create.TrackRef(edit_rate=edit_rate, media_kind='picture')
    track.filler_proxy.length = 2147483647

    clip = f.create.SourceClip(edit_rate=edit_rate, media_kind='picture')
    clip.length = length
    clip.mob_id = file_mob.mob_id
    clip.track_id = 1
    track.component = clip
    mob.length = length

    mob.tracks.append(track)

    f.content.add_mob(mob)
    f.content.add_mob(file_mob)
    f.content.add_mob(tape_mob)

    return mob

def create_sequence(result_file, mob_name, comp_name, track_id,  start_time, length):
    with avb.open() as f:
        edit_rate = 25
        initial_mob = create_mastermob(f, mob_name, start_time, length)

        comp = f.create.Composition(mob_type="CompositionMob")

        comp.name = comp_name

        # timecode track
        track = f.create.Track()
        track.index = 1
        track.component = f.create.Timecode(edit_rate=edit_rate, media_kind='timecode')
        track.component.start = 90000
        track.component.fps = 25
        track.component.length = 500
        comp.tracks.append(track)

        # Video
        track = f.create.Track()
        track.index = 1
        track.filler_proxy = f.create.TrackRef(edit_rate=edit_rate, media_kind='picture')
        track.filler_proxy.length = 2147483647
        track.filler_proxy.relative_scope = 0
        track.filler_proxy.relative_track

        sequence = f.create.Sequence(edit_rate=edit_rate, media_kind='picture')
        sequence.components.append(f.create.Filler(edit_rate=edit_rate, media_kind='picture'))

        clip = f.create.SourceClip(edit_rate=edit_rate, media_kind='picture')
        clip.track_id = track_id
        clip.start_time = start_time
        clip.length = length
        clip.mob_id = initial_mob.mob_id
        sequence.components.append(clip)

        fill = f.create.Filler(edit_rate=edit_rate, media_kind='picture')
        fill.length = length
        sequence.components.append(fill)

        track.component = sequence
        comp.tracks.append(track)
        comp.length = sequence.length

        # Audio
        track = f.create.Track()
        track.index = 1
        sequence = f.create.Sequence(edit_rate=edit_rate, media_kind='sound')
        fill = f.create.Filler(edit_rate=edit_rate, media_kind='sound')
        fill.length = comp.length
        sequence.components.append(fill)
        track.component = sequence
        comp.tracks.append(track)

        f.content.add_mob(comp)

        f.write(result_file)